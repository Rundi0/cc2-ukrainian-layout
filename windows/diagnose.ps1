<#
    Read-only.  Dumps everything that decides whether the layout is offered as
    a keyboard, then asks Windows to actually load it and type with it.
    Run in a normal (non-elevated) PowerShell and paste the whole output.
#>
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
# without this the Cyrillic in the key test prints as '?' in a cp1251 console
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$klid = 'a0000422'
$key  = "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\$klid"

Write-Host "=== Windows ===" -ForegroundColor Cyan
[Environment]::OSVersion.Version.ToString()
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').DisplayVersion

Write-Host "`n=== HKLM key $klid ===" -ForegroundColor Cyan
if (Test-Path $key) {
    Get-Item $key | Select-Object -ExpandProperty Property | ForEach-Object {
        '{0,-30} = {1}' -f $_, (Get-ItemProperty $key -Name $_).$_
    }
} else { Write-Host 'MISSING -- the layout is not registered at all' }

Write-Host "`n=== uacc.dll on disk ===" -ForegroundColor Cyan
foreach ($d in "$env:SystemRoot\System32", "$env:SystemRoot\SysWOW64") {
    $f = "$d\uacc.dll"
    if (Test-Path $f) {
        '{0,-40} {1} bytes  sha256={2}' -f $f, (Get-Item $f).Length,
            (Get-FileHash $f -Algorithm SHA256).Hash.Substring(0, 16)
    } else { "$f  MISSING" }
}

Write-Host "`n=== Layout Id collisions ===" -ForegroundColor Cyan
$mine = (Get-ItemProperty $key -Name 'Layout Id' -ErrorAction SilentlyContinue).'Layout Id'
Write-Host "ours = $mine"
Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts' | ForEach-Object {
    $id = (Get-ItemProperty $_.PSPath -Name 'Layout Id' -ErrorAction SilentlyContinue).'Layout Id'
    if ($id -and $id -eq $mine -and $_.PSChildName -ne $klid) {
        Write-Host ("COLLISION: {0} also uses Layout Id {1}" -f $_.PSChildName, $id) -ForegroundColor Red
    }
}

Write-Host "`n=== HKCU preload / substitutes ===" -ForegroundColor Cyan
foreach ($p in 'HKCU:\Keyboard Layout\Preload', 'HKCU:\Keyboard Layout\Substitutes') {
    Write-Host $p
    if (Test-Path $p) {
        Get-Item $p | Select-Object -ExpandProperty Property | ForEach-Object {
            '  {0,-6} = {1}' -f $_, (Get-ItemProperty $p -Name $_).$_
        }
    } else { Write-Host '  (absent)' }
}

Write-Host "`n=== user language list ===" -ForegroundColor Cyan
foreach ($l in @(Get-WinUserLanguageList)) {
    '{0}  tips: {1}' -f $l.LanguageTag, ($l.InputMethodTips -join ', ')
}

# ---------------------------------------------------------------------------
# The decisive test.  Everything above can be perfect and the layout still be
# unusable if win32k refuses the DLL.  Loading two stock layouts first is the
# control: if those fail too, the test itself is broken, not our layout.
# ---------------------------------------------------------------------------
Write-Host "`n=== can Windows load and use it? ===" -ForegroundColor Cyan
Add-Type -Namespace Kbd -Name N -MemberDefinition @'
[DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
public static extern IntPtr LoadKeyboardLayout(string klid, uint flags);
[DllImport("user32.dll", SetLastError=true)]
public static extern bool UnloadKeyboardLayout(IntPtr hkl);
[DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
public static extern int ToUnicodeEx(uint vk, uint sc, byte[] state,
    System.Text.StringBuilder buf, int cch, uint flags, IntPtr hkl);
[DllImport("user32.dll")]
public static extern uint MapVirtualKeyEx(uint code, uint mapType, IntPtr hkl);
'@

# KLF_ACTIVATE 0x1, KLF_SUBSTITUTE_OK 0x2, KLF_NOTELLSHELL 0x80
function Try-Load($id, $flags, $label) {
    $h = [Kbd.N]::LoadKeyboardLayout($id, $flags)
    $e = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if ($h -eq [IntPtr]::Zero) {
        Write-Host ("  {0,-34} NULL (err {1})" -f $label, $e) -ForegroundColor Red
        return [IntPtr]::Zero
    }
    Write-Host ("  {0,-34} HKL 0x{1:X8}" -f $label, ($h.ToInt64() -band 0xFFFFFFFF)) -ForegroundColor Green
    return $h
}

Write-Host "control -- these must succeed:"
[void](Try-Load '00000409' 0x80 'US English (stock)')
[void](Try-Load '00000422' 0x80 'Ukrainian (stock)')

Write-Host "ours:"
$hkl = [IntPtr]::Zero
foreach ($t in @(@('a0000422', 0x80, 'a0000422 NOTELLSHELL'),
                 @('a0000422', 0x81, 'a0000422 ACTIVATE'),
                 @('a0000422', 0x82, 'a0000422 SUBSTITUTE_OK'),
                 @('d0010422', 0x82, 'd0010422 (preload id)'))) {
    $h = Try-Load $t[0] $t[1] $t[2]
    if ($hkl -eq [IntPtr]::Zero) { $hkl = $h }
}

if ($hkl -ne [IntPtr]::Zero) {
    $v = $hkl.ToInt64() -band 0xFFFFFFFF
    if (($v -shr 16) -ne 0xF0C0) {
        Write-Host ("  WARNING: high word 0x{0:X4}, expected 0xF0C0 -- Windows substituted another layout" -f ($v -shr 16)) -ForegroundColor Yellow
    }
    # Ask the loaded DLL what every key produces on every level and compare
    # against expected.tsv, which gen.py writes from the same table the DLL is
    # generated from.  This is the check that says "yes, this is the layout".
    $exp = Join-Path $here 'expected.tsv'
    if (-not (Test-Path $exp)) { Write-Warning "no $exp, skipping key test"; return }

    $levelName = 'base', 'shift', 'altgr', 'shift+altgr'
    $bad = @()
    $n   = 0
    foreach ($line in Get-Content $exp) {
        if ($line.StartsWith('#')) { continue }
        $f     = $line.Split("`t")
        $sc    = [Convert]::ToUInt32($f[0], 16)
        $lvl   = [int]$f[1]
        $want  = [string][char][Convert]::ToInt32($f[2], 16)
        $vk    = [Kbd.N]::MapVirtualKeyEx($sc, 3, $hkl)   # MAPVK_VSC_TO_VK_EX

        $st = New-Object byte[] 256
        if ($lvl -band 1) { $st[0x10] = 0x80 }                    # Shift
        if ($lvl -band 2) { $st[0x11] = 0x80; $st[0x12] = 0x80 }  # Ctrl+Alt = AltGr

        $sb  = New-Object Text.StringBuilder 8
        $r   = [Kbd.N]::ToUnicodeEx($vk, $sc, $st, $sb, 8, 0, $hkl)
        $got = if ($r -gt 0) { $sb.ToString() } else { "(none, n=$r)" }
        $n++
        if ($got -ne $want) {
            $bad += "sc {0:X2} {1,-11} -> '{2}'  expected '{3}'" -f $sc, $levelName[$lvl], $got, $want
        }
    }

    if ($bad) {
        Write-Host ("  {0} of {1} keys WRONG:" -f $bad.Count, $n) -ForegroundColor Red
        $bad | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
    } else {
        Write-Host ("  all {0} key/level combinations match expected.tsv" -f $n) -ForegroundColor Green
    }
}
