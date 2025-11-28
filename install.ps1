# MergePDF 快速安裝腳本

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MergePDF - 快速安裝依賴套件" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Python 是否存在
try {
    $pythonVersion = python --version 2>&1
    Write-Host "找到 Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "錯誤: 找不到 Python！請先安裝 Python 3.8 或更高版本。" -ForegroundColor Red
    Read-Host "按 Enter 繼續"
    exit 1
}

# 確保在虛擬環境中
if (-not (Test-Path ".\Scripts\activate.ps1")) {
    Write-Host "虛擬環境不存在，正在建立..." -ForegroundColor Yellow
    python -m venv .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "建立虛擬環境失敗！" -ForegroundColor Red
        Read-Host "按 Enter 繼續"
        exit 1
    }
    Write-Host "虛擬環境建立成功！" -ForegroundColor Green
}

Write-Host ""
Write-Host "正在啟動虛擬環境..." -ForegroundColor Green
& ".\Scripts\Activate.ps1"

Write-Host ""
Write-Host "正在安裝依賴套件..." -ForegroundColor Green
Write-Host "這可能需要幾分鐘時間..." -ForegroundColor Yellow
Write-Host ""

pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "安裝完成！" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "現在可以執行以下命令啟動程式：" -ForegroundColor Cyan
    Write-Host "  .\run.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "或直接執行：" -ForegroundColor Cyan
    Write-Host "  python main.py" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "安裝失敗！請檢查錯誤訊息。" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "按 Enter 繼續"
