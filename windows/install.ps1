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

# uacc.dll is cross-compiled from windows\src\uacc.c by the `windows` GitHub
# Actions workflow, which commits the result back.  If you are on a commit CI
# has not caught up with yet, the DLL here predates the source -- installing it
# would silently give you the OLD layout, so refuse.
$src = Join-Path $here 'src\uacc.c'
$stampFile = "$here\built-from.sha256"
if ((Test-Path $src) -and (Test-Path $stampFile)) {
    $now   = (Get-FileHash $src -Algorithm SHA256).Hash
    $built = (Get-Content $stampFile -Raw).Trim()
    if ($now -ne $built) {
        Write-Warning 'uacc.dll is STALE: windows\src\uacc.c changed since it was built.'
        Write-Warning 'Installing it would give you the OLD layout.'
        Write-Warning 'Wait for the `windows` workflow to finish, then: git pull'
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
