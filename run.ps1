# MergePDF 執行腳本

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MergePDF - 檔案合併工具" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 確保在虛擬環境中
if (-not (Test-Path ".\Scripts\activate.ps1")) {
    Write-Host "錯誤: 找不到虛擬環境！" -ForegroundColor Red
    Write-Host "請先執行: python -m venv venv" -ForegroundColor Yellow
    Write-Host "然後執行: .\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "最後執行: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "按 Enter 繼續"
    exit 1
}

Write-Host "正在啟動虛擬環境..." -ForegroundColor Green
& ".\Scripts\Activate.ps1"

Write-Host "正在啟動 MergePDF..." -ForegroundColor Green
Write-Host ""

python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "程式執行時發生錯誤！" -ForegroundColor Red
    Read-Host "按 Enter 繼續"
}
