# MergePDF Nuitka 編譯腳本 - PySide6 版本

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MergePDF - Nuitka 編譯腳本 (PySide6)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 確保在虛擬環境中
if (-not (Test-Path ".\Scripts\activate.ps1")) {
    Write-Host "錯誤: 找不到虛擬環境！" -ForegroundColor Red
    Write-Host "請先執行: python -m venv venv" -ForegroundColor Yellow
    Read-Host "按 Enter 繼續"
    exit 1
}

Write-Host "正在啟動虛擬環境..." -ForegroundColor Green
& ".\Scripts\Activate.ps1"

Write-Host ""
Write-Host "開始使用 Nuitka 編譯..." -ForegroundColor Green
Write-Host ""

# 使用 Nuitka 編譯 - PySide6 版本
python -m nuitka `
    --standalone `
    --onefile `
    --windows-console-mode=disable `
    --enable-plugin=pyside6 `
    --company-name="MergePDF" `
    --product-name="MergePDF" `
    --file-version=1.0.0.0 `
    --product-version=1.0.0 `
    --file-description="檔案合併為 PDF 工具 (PySide6)" `
    --output-filename=MergePDF.exe `
    --output-dir=dist `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "編譯成功！" -ForegroundColor Green
    Write-Host "執行檔位置: dist\MergePDF.exe" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "編譯失敗！請檢查錯誤訊息。" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "按 Enter 繼續"
