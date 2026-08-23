<#
    Read-only.  Dumps everything that decides whether the layout is offered as
    a keyboard, then asks Windows to actually load it and type with it.
    Run in a normal (non-elevated) PowerShell and paste the whole output.
#>
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
Get-WinUserLanguageList | ForEach-Object {
    '{0}  tips: {1}' -f $_.LanguageTag, ($_.InputMethodTips -join ', ')
}

# ---------------------------------------------------------------------------
# The decisive test: everything above can be perfect and the layout still be
# unusable if win32k refuses the DLL.  Ask Windows to load it and type with it.
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
'@

$hkl = [Kbd.N]::LoadKeyboardLayout($klid, 0x100)   # KLF_NOTELLSHELL
if ($hkl -eq [IntPtr]::Zero) {
    $e = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
    Write-Host "LoadKeyboardLayout FAILED, error $e" -ForegroundColor Red
    Write-Host ([ComponentModel.Win32Exception]::new($e).Message) -ForegroundColor Red
} else {
    $v = $hkl.ToInt64() -band 0xFFFFFFFF
    Write-Host ("LoadKeyboardLayout ok, HKL = 0x{0:X8}" -f $v)
    if (($v -shr 16) -ne 0xF0C0) {
        Write-Host ("  WARNING: high word is 0x{0:X4}, expected 0xF0C0 -- Windows substituted another layout" -f ($v -shr 16)) -ForegroundColor Yellow
    }
    function Type($vk, $sc, $altgr, $expect, $what) {
        $st = New-Object byte[] 256
        if ($altgr) { $st[0x11] = 0x80; $st[0x12] = 0x80 }   # Ctrl+Alt = AltGr
        $sb = New-Object Text.StringBuilder 8
        $n = [Kbd.N]::ToUnicodeEx($vk, $sc, $st, $sb, 8, 0, $hkl)
        $got = if ($n -gt 0) { $sb.ToString() } else { "(nothing, n=$n)" }
        $ok = if ($got -eq $expect) { 'OK ' } else { 'BAD' }
        $col = if ($got -eq $expect) { 'Green' } else { 'Red' }
        Write-Host ("  {0} {1,-18} -> '{2}'  expected '{3}'" -f $ok, $what, $got, $expect) -ForegroundColor $col
    }
    Type 0x43 0x2E $false 'ц' 'C'
    Type 0x43 0x2E $true  'ї' 'AltGr+C'
    Type 0x42 0x30 $true  'ю' 'AltGr+B'
    Type 0xBC 0x33 $false ',' 'comma key'
    [void][Kbd.N]::UnloadKeyboardLayout($hkl)
}
