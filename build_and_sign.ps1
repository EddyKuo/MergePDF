# MergePDF 完整建置與簽章流程

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MergePDF - 完整建置與簽章" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 步驟 1: 建立憑證（如果不存在）
$configFile = ".\certificate_config.txt"

if (-not (Test-Path $configFile)) {
    Write-Host "步驟 1/3: 建立數位憑證..." -ForegroundColor Green
    Write-Host ""
    & ".\create_certificate.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "建立憑證失敗，無法繼續" -ForegroundColor Red
        Read-Host "按 Enter 繼續"
        exit 1
    }
} else {
    Write-Host "步驟 1/3: 使用現有憑證" -ForegroundColor Green
    Write-Host ""
}

# 步驟 2: 編譯程式
Write-Host "步驟 2/3: 編譯程式..." -ForegroundColor Green
Write-Host ""

$buildChoice = Read-Host "選擇編譯方式: [1] 簡易版 [2] 完整版 (預設: 1)"

if ($buildChoice -eq "2") {
    & ".\build.ps1"
} else {
    & ".\build_simple.ps1"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "編譯失敗，無法繼續" -ForegroundColor Red
    Read-Host "按 Enter 繼續"
    exit 1
}

# 步驟 3: 簽署執行檔
Write-Host ""
Write-Host "步驟 3/3: 簽署執行檔..." -ForegroundColor Green
Write-Host ""

& ".\sign_exe.ps1"

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "完成！" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "已簽署的執行檔: dist\MergePDF.exe" -ForegroundColor Cyan
Write-Host ""

Read-Host "按 Enter 繼續"
