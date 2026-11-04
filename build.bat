@echo off
chcp 65001 >nul
setlocal
title 远程之门 - 一键构建
cd /d "%~dp0"

set "PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装排版依赖 reportlab ...
    "%PY%" -m pip install --quiet reportlab
)

echo.
echo ==================================================
echo   远程之门   构建开始
echo ==================================================

echo [1/4] 重新生成插图
for /d %%D in (book\code\ch*) do (
    if exist "%%D\figs.py" (
        "%PY%" "%%D\figs.py" >nul 2>&1
        if errorlevel 1 echo       [!] %%~nxD 的插图生成失败
    )
)
if exist "book\code\common\make_cover.py" (
    "%PY%" "book\code\common\make_cover.py" >nul 2>&1
)

echo [2/4] 检查稿件
"%PY%" book\build\lint.py
if errorlevel 1 goto :fail

echo [3/4] 编译 PDF
"%PY%" book\build\build.py
if errorlevel 1 goto :fail

echo [4/4] 完成
echo.
echo   PDF 输出： output\remote-access-book.pdf
echo   在线阅读： 打开仓库根目录的 index.html 或访问 GitHub Pages
echo.
pause
exit /b 0

:fail
echo.
echo [失败] 构建中止，请查看上面的错误信息。
pause
exit /b 1
