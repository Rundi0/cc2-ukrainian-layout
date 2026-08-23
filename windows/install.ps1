#Requires -RunAsAdministrator
<#
    Installs the Ukrainian (CharaChorder Two) keyboard layout.

    Everything needed is in this folder -- MSKLC is only required to *produce*
    uacc.dll, never to install it.
#>
param([switch]$Force)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$klid = 'a0000422'

# The shipped DLL is built by MSKLC from out\ua_cc.klc.  gen.py can change the
# .klc without anyone rebuilding the DLL, and a stale DLL installs silently as
# the *old* layout -- so compare what the DLL was built from against what is in
# the tree now.
$klc = Join-Path (Split-Path -Parent $here) 'out\ua_cc.klc'
$stampFile = "$here\built-from.sha256"
if ((Test-Path $klc) -and (Test-Path $stampFile)) {
    $now   = (Get-FileHash $klc -Algorithm SHA256).Hash
    $built = (Get-Content $stampFile -Raw).Trim()
    if ($now -ne $built) {
        Write-Warning 'uacc.dll is STALE: out\ua_cc.klc changed since it was built.'
        Write-Warning 'Installing it would give you the OLD layout.'
        Write-Warning 'Rebuild: open out\ua_cc.klc in MSKLC -> Project -> Build DLL and'
        Write-Warning 'Setup Package, copy the new DLLs into windows\amd64 and windows\i386,'
        Write-Warning "then write the new hash into windows\built-from.sha256:"
        Write-Warning "    (Get-FileHash out\ua_cc.klc -Algorithm SHA256).Hash > windows\built-from.sha256"
        if (-not $Force) {
            throw 'refusing to install a stale layout; pass -Force to override'
        }
    }
}

$targets = @(
    @{ dll = "$here\amd64\uacc.dll"; dst = "$env:SystemRoot\System32"  }
    @{ dll = "$here\i386\uacc.dll";  dst = "$env:SystemRoot\SysWOW64"  }
)
foreach ($t in $targets) {
    if (-not (Test-Path $t.dll)) { throw "missing $($t.dll)" }
    Copy-Item $t.dll $t.dst -Force
    Write-Host "installed $($t.dst)\uacc.dll"
}

reg.exe import "$here\uacc.reg" | Out-Null
Write-Host "registered $klid"

# MSKLC 1.4 points Layout Display Name at a string resource it never puts in
# the DLL; Windows 11 then lists the layout as "Unavailable input method".
# Dropping the value makes Windows fall back to Layout Text.
$key = "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\$klid"
Remove-ItemProperty $key -Name 'Layout Display Name' -ErrorAction SilentlyContinue

Get-ItemProperty $key | Format-List 'Layout File', 'Layout Text', 'Layout Id'
Write-Host ''
Write-Host 'Sign out and back in, then: Settings -> Time & language -> Language'
Write-Host '-> Ukrainian -> Language options -> Add a keyboard.'
