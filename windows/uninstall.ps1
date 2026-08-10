#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
$klid = 'a0000422'

Remove-Item "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\$klid" `
    -Recurse -ErrorAction SilentlyContinue
foreach ($d in "$env:SystemRoot\System32", "$env:SystemRoot\SysWOW64") {
    Remove-Item "$d\uacc.dll" -Force -ErrorAction SilentlyContinue
}
Write-Host 'Removed. Sign out and back in.'
Write-Host 'If the layout is still listed, drop it under Language options first.'
