@echo off
REM MergePDF Nuitka 簡易編譯腳本 - PySide6 版本

echo ================================================
echo MergePDF - Nuitka 簡易編譯 (PySide6)
echo ================================================
echo.

REM 確保在虛擬環境中
if not exist "venv\Scripts\activate.bat" (
    echo 錯誤: 找不到虛擬環境！
    echo 請先執行: python -m venv venv
    pause
    exit /b 1
)

echo 正在啟動虛擬環境...
call venv\Scripts\activate.bat

echo.
echo 開始使用 Nuitka 編譯...
echo 注意：PySide6 編譯時間較長，請耐心等候...
echo.

REM 使用 Nuitka 編譯（簡化版）- PySide6
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --enable-plugin=pyside6 ^
    --output-filename=MergePDF.exe ^
    --output-dir=dist ^
    main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo 編譯成功！
    echo 執行檔位置: dist\MergePDF.exe
    echo ================================================
    echo.
    echo 您可以直接執行: dist\MergePDF.exe
) else (
    echo.
    echo ================================================
    echo 編譯失敗！請檢查錯誤訊息。
    echo ================================================
)

echo.
pause
