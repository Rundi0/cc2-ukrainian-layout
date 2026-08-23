@echo off
rem  %1 = vcvarsall arch (x64 / x86)   %2 = output dir   %3 = image base
setlocal
for /f "usebackq tokens=*" %%i in (`"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "VSPATH=%%i"
if not defined VSPATH ( echo cannot locate Visual Studio & exit /b 1 )

call "%VSPATH%\VC\Auxiliary\Build\vcvarsall.bat" %1 || exit /b 1

rem /DYNAMICBASE:NO does not clear high-entropy ASLR on x64; it needs its own
rem switch, and the switch only exists for 64-bit targets.
set "EXTRA="
if /i "%1"=="x64" set "EXTRA=/HIGHENTROPYVA:NO"

set "SRC=%~dp0"
rem %~dp0 ends in a backslash, which would escape the closing quote of /I
set "SRCD=%SRC:~0,-1%"
if not exist "%SRC%..\%2" mkdir "%SRC%..\%2"

rc /nologo /fo "%TEMP%\uacc_%2.res" "%SRC%uacc.rc" || exit /b 1

rem /GS- and /NODEFAULTLIB because nothing from the CRT may be linked in:
rem a layout DLL is mapped by win32k and must import nothing.
cl /nologo /c /O1 /GS- /Gy- /I"%SRCD%" /Fo"%TEMP%\uacc_%2.obj" "%SRC%uacc.c" || exit /b 1

link /nologo /DLL /NOENTRY /NODEFAULTLIB /SUBSYSTEM:NATIVE ^
     /MERGE:.rdata=.data /MERGE:.bss=.data /IGNORE:4254 ^
     /BASE:%3 /DYNAMICBASE:NO /NXCOMPAT:NO %EXTRA% ^
     /EXPORT:KbdLayerDescriptor ^
     /OUT:"%SRC%..\%2\uacc.dll" "%TEMP%\uacc_%2.obj" "%TEMP%\uacc_%2.res" || exit /b 1

echo built %2\uacc.dll
