# 簽署 MergePDF.exe 執行檔

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MergePDF - 數位簽章工具" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 檢查執行檔是否存在
$exePath = ".\dist\MergePDF.exe"

if (-not (Test-Path $exePath)) {
    Write-Host "✗ 錯誤: 找不到執行檔 $exePath" -ForegroundColor Red
    Write-Host "請先執行 build_simple.ps1 編譯程式" -ForegroundColor Yellow
    Read-Host "按 Enter 繼續"
    exit 1
}

Write-Host "找到執行檔: $exePath" -ForegroundColor Green
Write-Host ""

# 讀取憑證指紋
$configFile = ".\certificate_config.txt"

if (Test-Path $configFile) {
    $thumbprint = (Get-Content $configFile -Raw).Trim()
    Write-Host "使用儲存的憑證指紋: $thumbprint" -ForegroundColor Green
} else {
    Write-Host "找不到憑證設定檔，請先執行 create_certificate.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "或手動輸入憑證指紋:" -ForegroundColor Cyan
    $thumbprint = Read-Host "憑證指紋"
    
    if ([string]::IsNullOrWhiteSpace($thumbprint)) {
        Write-Host "✗ 未提供憑證指紋" -ForegroundColor Red
        Read-Host "按 Enter 繼續"
        exit 1
    }
}

# 取得憑證
Write-Host ""
Write-Host "正在載入憑證..." -ForegroundColor Green

try {
    $cert = Get-ChildItem -Path Cert:\CurrentUser\My\$thumbprint -ErrorAction Stop
    Write-Host "✓ 憑證載入成功" -ForegroundColor Green
    Write-Host "  主旨: $($cert.Subject)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "✗ 找不到憑證，請確認指紋是否正確" -ForegroundColor Red
    Write-Host "可用的憑證列表:" -ForegroundColor Yellow
    Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object { $_.Subject -like "*MergePDF*" } | Format-Table Subject, Thumbprint -AutoSize
    Read-Host "按 Enter 繼續"
    exit 1
}

# 簽署執行檔
Write-Host "正在簽署執行檔..." -ForegroundColor Green

try {
    # 使用 Set-AuthenticodeSignature 簽署
    $signature = Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
    
    if ($signature.Status -eq "Valid") {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Green
        Write-Host "✓ 簽署成功！" -ForegroundColor Green
        Write-Host "================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "簽章資訊:" -ForegroundColor Cyan
        Write-Host "  檔案: $exePath" -ForegroundColor White
        Write-Host "  簽章者: $($cert.Subject)" -ForegroundColor White
        Write-Host "  狀態: $($signature.Status)" -ForegroundColor White
        
        # 檢查簽章
        Write-Host ""
        Write-Host "驗證簽章..." -ForegroundColor Green
        $verify = Get-AuthenticodeSignature -FilePath $exePath
        Write-Host "  驗證狀態: $($verify.Status)" -ForegroundColor White
        Write-Host ""
        
        if ($verify.Status -eq "Valid") {
            Write-Host "✓ 數位簽章驗證通過" -ForegroundColor Green
        } else {
            Write-Host "⚠ 警告: $($verify.StatusMessage)" -ForegroundColor Yellow
        }
        
    } else {
        Write-Host "✗ 簽署失敗: $($signature.StatusMessage)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "✗ 簽署時發生錯誤: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "注意事項:" -ForegroundColor Cyan
Write-Host "  • 自簽章憑證只適用於開發和測試" -ForegroundColor White
Write-Host "  • 使用者首次執行時可能仍會看到 SmartScreen 警告" -ForegroundColor White
Write-Host "  • 若要正式發布，建議購買商業代碼簽章憑證" -ForegroundColor White
Write-Host ""

Read-Host "按 Enter 繼續"
