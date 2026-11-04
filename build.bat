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

echo.
echo ==================================================
echo   Building the book
echo ==================================================

echo [1/4] rendering figures
for /d %%D in (book\code\ch*) do (
    if exist "%%D\figs.py" (
        "%PY%" "%%D\figs.py" >nul 2>&1
        if errorlevel 1 echo       [!] %%~nxD figures failed
    )
)
if exist "book\code\common\make_cover.py" (
    "%PY%" "book\code\common\make_cover.py" >nul 2>&1
)

echo [2/4] checking manuscript
"%PY%" book\build\lint.py
if errorlevel 1 goto :fail

echo [3/4] typesetting PDF
"%PY%" book\build\build.py
if errorlevel 1 goto :fail

echo [4/4] done
echo.
echo   PDF    : output\remote-access-book.pdf
echo   Web    : open index.html, or push and use GitHub Pages
echo.
pause
exit /b 0

:fail
echo.
echo [failed] build stopped. See the messages above.
pause
exit /b 1
