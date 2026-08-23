<#
    Adds the layout to the CURRENT USER's language list.

    Windows 11 often does not offer a custom layout under "Add a keyboard" at
    all, even when it is correctly registered machine-wide.  Setting the input
    method tip directly is the reliable route.  Per-user, so run this WITHOUT
    elevation, as the account you actually type in.
#>
$ErrorActionPreference = 'Stop'
$tip = '0422:A0000422'          # Ukrainian language id : our KLID

$list = Get-WinUserLanguageList
$uk = $list | Where-Object { $_.LanguageTag -like 'uk*' } | Select-Object -First 1
if (-not $uk) {
    $list.Add('uk-UA')
    $uk = $list | Where-Object { $_.LanguageTag -like 'uk*' } | Select-Object -First 1
    Write-Host 'added Ukrainian to the language list'
}
if ($uk.InputMethodTips -notcontains $tip) {
    $uk.InputMethodTips.Add($tip)
    Write-Host "added input method $tip"
} else {
    Write-Host "$tip was already present"
}
Set-WinUserLanguageList $list -Force

Write-Host ''
Get-WinUserLanguageList | ForEach-Object {
    '{0}  tips: {1}' -f $_.LanguageTag, ($_.InputMethodTips -join ', ')
}
Write-Host ''
Write-Host 'Sign out and back in, then check Win+Space.'
