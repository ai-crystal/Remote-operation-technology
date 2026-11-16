@echo off
chcp 65001 >nul
setlocal
title Remote Gateway - Build
cd /d "%~dp0"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

set "PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    echo [info] installing reportlab ...
    "%PY%" -m pip install --quiet reportlab
)

rem usage:
rem   build.bat              build all three books
rem   build.bat beginner     build beginner volume only
rem   build.bat intermediate build intermediate volume only
rem   build.bat deep         build deep volume only
rem   build.bat figures      re-render figures (affects intermediate only)

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=all"

if /i "%TARGET%"=="all" goto :all
if /i "%TARGET%"=="figures" goto :figures
if /i "%TARGET%"=="beginner" goto :one_arg
if /i "%TARGET%"=="intermediate" goto :one_arg
if /i "%TARGET%"=="deep" goto :one_arg

echo Unknown volume: %TARGET%
echo Choose one of: beginner / intermediate / deep / figures / all
goto :fail

:all
call :one beginner
if errorlevel 1 goto :fail
call :one intermediate
if errorlevel 1 goto :fail
call :one deep
if errorlevel 1 goto :fail
goto :done

:one_arg
call :one %TARGET%
if errorlevel 1 goto :fail
goto :done

:one
set "NAME=%~1"
if "%NAME%"=="" set "NAME=%TARGET%"
echo.
echo ==================================================
echo   Building %NAME%
echo ==================================================
"%PY%" book\build\lint.py --book book\%NAME%
if errorlevel 1 exit /b 1
"%PY%" book\build\build.py --book book\%NAME%
if errorlevel 1 exit /b 1
exit /b 0

:figures
echo [figures] rendering all diagrams
for /d %%D in (book\code\ch*) do (
    if exist "%%D\figs.py" (
        "%PY%" "%%D\figs.py" >nul 2>&1
        if errorlevel 1 echo       [!] %%~nxD figures failed
    )
)
echo [figures] done. beginner/deep use copied images; sync them by hand if needed.
exit /b 0

:done
echo.
echo ==================================================
echo   Done
echo ==================================================
echo   PDF : output\remote-gate-beginner.pdf
echo         output\remote-access-book.pdf
echo         output\remote-gate-deep.pdf
echo.
pause
exit /b 0

:fail
echo.
echo [failed] build stopped. See the messages above.
pause
exit /b 1
