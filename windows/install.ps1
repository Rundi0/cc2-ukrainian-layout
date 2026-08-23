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
    # normalise line endings first -- git hands out CRLF or LF depending on
    # core.autocrlf, and a raw file hash would differ between clones
    $bytes = [Text.Encoding]::UTF8.GetBytes(
        ([IO.File]::ReadAllText($src) -replace "`r`n", "`n"))
    $now   = (Get-FileHash -InputStream ([IO.MemoryStream]::new($bytes)) `
                           -Algorithm SHA256).Hash
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

# reg.exe import adds and overwrites, but never deletes.  Earlier versions of
# this layout were registered from an MSKLC export that named two string
# resources (-1000, -1100) which our DLL does not contain.  Windows cannot
# resolve them, and an input method with an unresolvable display name is shown
# under Language options but never offered as a keyboard -- so clear them out.
$key = "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\$klid"
foreach ($stale in 'Layout Display Name', 'Custom Language Name',
                   'Custom Language Display Name', 'Layout Product Code') {
    if ($null -ne (Get-ItemProperty $key -Name $stale -ErrorAction SilentlyContinue)) {
        Remove-ItemProperty $key -Name $stale
        Write-Host "removed stale '$stale'"
    }
}

Get-ItemProperty $key | Format-List 'Layout File', 'Layout Text', 'Layout Id'
Write-Host ''
Write-Host 'Sign out and back in, then: Settings -> Time & language -> Language'
Write-Host '-> Ukrainian -> Language options -> Add a keyboard.'
