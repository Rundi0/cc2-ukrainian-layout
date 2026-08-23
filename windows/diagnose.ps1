<#
    Read-only.  Dumps everything that decides whether the layout is offered as
    a keyboard.  Run it in a normal (non-elevated) PowerShell and paste the
    whole output.
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
# Windows silently ignores a layout whose Layout Id is already taken.
$mine = (Get-ItemProperty $key -Name 'Layout Id' -ErrorAction SilentlyContinue).'Layout Id'
Write-Host "ours = $mine"
Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts' | ForEach-Object {
    $id = (Get-ItemProperty $_.PSPath -Name 'Layout Id' -ErrorAction SilentlyContinue).'Layout Id'
    if ($id -and $id -eq $mine -and $_.PSChildName -ne $klid) {
        Write-Host ("COLLISION: {0} also uses Layout Id {1} ({2})" -f $_.PSChildName, $id,
            (Get-ItemProperty $_.PSPath -Name 'Layout Text' -ErrorAction SilentlyContinue).'Layout Text') -ForegroundColor Red
    }
}

Write-Host "`n=== HKCU preload / substitutes ===" -ForegroundColor Cyan
Get-ItemProperty 'HKCU:\Keyboard Layout\Preload' -ErrorAction SilentlyContinue |
    Format-List * -Exclude PS*
Get-ItemProperty 'HKCU:\Keyboard Layout\Substitutes' -ErrorAction SilentlyContinue |
    Format-List * -Exclude PS*

Write-Host "=== user language list ===" -ForegroundColor Cyan
Get-WinUserLanguageList | ForEach-Object {
    '{0}  tips: {1}' -f $_.LanguageTag, ($_.InputMethodTips -join ', ')
}
