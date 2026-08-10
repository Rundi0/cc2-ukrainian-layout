#Requires -RunAsAdministrator
<#
    Installs the Ukrainian (CharaChorder Two) keyboard layout.

    Everything needed is in this folder -- MSKLC is only required to *produce*
    uacc.dll, never to install it.
#>
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$klid = 'a0000422'

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
