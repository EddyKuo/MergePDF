# MergePDF 數位簽章指南

## 概述

本指南說明如何為 MergePDF.exe 添加數位簽章。數位簽章可以：
- ✅ 證明程式來源的真實性
- ✅ 確保程式未被竄改
- ✅ 減少 Windows SmartScreen 警告（部分）

## 📋 簽章類型

### 1. 自簽章憑證（開發測試用）
- **優點**：免費、快速建立
- **缺點**：使用者首次執行仍會看到警告
- **適用**：個人使用、內部測試

### 2. 商業代碼簽章憑證（正式發布用）
- **優點**：受 Windows 信任、減少警告
- **缺點**：需要購買（約 USD 100-500/年）
- **適用**：公開發布、商業軟體

## 🚀 快速開始（自簽章）

### 一鍵完成（推薦）

```powershell
.\build_and_sign.ps1
```

這會自動：
1. 建立憑證（如果不存在）
2. 編譯程式
3. 簽署執行檔

### 分步執行

#### 步驟 1: 建立自簽章憑證

```powershell
.\create_certificate.ps1
```

這會：
- 建立一個 3 年有效期的代碼簽章憑證
- 儲存憑證指紋到 `certificate_config.txt`
- 可選：安裝到信任的根憑證授權單位

#### 步驟 2: 編譯程式

```powershell
.\build_simple.ps1
```

#### 步驟 3: 簽署執行檔

```powershell
.\sign_exe.ps1
```

## 📖 詳細說明

### 自簽章憑證的建立

腳本會建立包含以下資訊的憑證：
- **主旨**: CN=MergePDF,O=MergePDF Development,C=TW
- **類型**: CodeSigningCert
- **有效期**: 3 年
- **儲存位置**: Cert:\CurrentUser\My

### 簽章過程

1. **載入憑證**：從憑證存放區讀取
2. **簽署檔案**：使用 `Set-AuthenticodeSignature`
3. **時間戳記**：使用 DigiCert 時間戳記伺服器
4. **驗證**：自動驗證簽章狀態

### 時間戳記的重要性

時間戳記確保：
- 即使憑證過期，簽章仍然有效
- 證明簽章時憑證是有效的

## 🔒 進階：使用商業憑證

### 購買代碼簽章憑證

推薦的憑證供應商：
1. **DigiCert** (https://www.digicert.com)
2. **Sectigo** (https://www.sectigo.com)
3. **GlobalSign** (https://www.globalsign.com)

### 使用商業憑證簽章

如果您有 `.pfx` 或 `.p12` 憑證檔案：

```powershell
# 匯入憑證
$pfxPath = "C:\path\to\your\certificate.pfx"
$pfxPassword = Read-Host "輸入憑證密碼" -AsSecureString
Import-PfxCertificate -FilePath $pfxPath -CertStoreLocation Cert:\CurrentUser\My -Password $pfxPassword

# 簽署（使用憑證指紋）
$cert = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object { $_.Subject -like "*Your Company*" }
Set-AuthenticodeSignature -FilePath ".\dist\MergePDF.exe" -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
```

### 使用 SignTool（Windows SDK）

如果您有安裝 Windows SDK：

```cmd
signtool sign /f "certificate.pfx" /p "password" /t http://timestamp.digicert.com /fd SHA256 "dist\MergePDF.exe"
```

## ⚠️ 注意事項

### 自簽章憑證

1. **安裝憑證到根存放區**
   - 執行 `create_certificate.ps1` 時選擇 "Y"
   - 或手動：
     ```powershell
     $cert = Get-ChildItem -Path Cert:\CurrentUser\My\[指紋]
     Export-Certificate -Cert $cert -FilePath temp.cer
     Import-Certificate -FilePath temp.cer -CertStoreLocation Cert:\CurrentUser\Root
     ```

2. **SmartScreen 警告**
   - 自簽章憑證無法完全避免 SmartScreen
   - 需要建立「信譽」（下載次數、使用者回饋）
   - 或購買 EV (Extended Validation) 憑證

3. **憑證有效期**
   - 預設 3 年
   - 到期前需重新建立並簽署

### 商業憑證

1. **憑證類型選擇**
   - **標準代碼簽章**：較便宜，但有 SmartScreen
   - **EV 代碼簽章**：較貴，立即受信任

2. **硬體 Token**
   - EV 憑證通常儲存在硬體 USB Token 中
   - 簽章時需要插入 Token

3. **組織驗證**
   - 需要提供公司文件
   - 審核時間約 1-7 天

## 🔍 驗證簽章

### 在 Windows 檔案總管

1. 右鍵點擊 `MergePDF.exe`
2. 選擇「屬性」
3. 切換到「數位簽章」標籤
4. 查看簽章詳細資訊

### 使用 PowerShell

```powershell
# 檢查簽章
Get-AuthenticodeSignature -FilePath ".\dist\MergePDF.exe"

# 顯示詳細資訊
Get-AuthenticodeSignature -FilePath ".\dist\MergePDF.exe" | Format-List *
```

### 使用 SignTool

```cmd
signtool verify /pa dist\MergePDF.exe
```

## 📚 相關資源

- [Microsoft 代碼簽章文件](https://docs.microsoft.com/windows/win32/seccrypto/cryptography-tools)
- [DigiCert 時間戳記伺服器](http://timestamp.digicert.com)
- [Windows SDK 下載](https://developer.microsoft.com/windows/downloads/windows-sdk/)

## 🆘 疑難排解

### 問題：找不到憑證

**解決**：
```powershell
# 列出所有個人憑證
Get-ChildItem -Path Cert:\CurrentUser\My

# 列出代碼簽章憑證
Get-ChildItem -Path Cert:\CurrentUser\My -CodeSigningCert
```

### 問題：簽章失敗

**可能原因**：
1. 憑證已過期
2. 憑證不是代碼簽章類型
3. 沒有私密金鑰

**檢查**：
```powershell
$cert = Get-ChildItem -Path Cert:\CurrentUser\My\[指紋]
$cert.NotAfter  # 檢查有效期
$cert.HasPrivateKey  # 檢查私密金鑰
```

### 問題：時間戳記失敗

**解決**：
- 檢查網路連線
- 嘗試其他時間戳記伺服器：
  - http://timestamp.digicert.com
  - http://timestamp.globalsign.com
  - http://timestamp.comodoca.com

---

**提示**：對於正式發布的軟體，強烈建議使用 EV 代碼簽章憑證以獲得最佳使用者體驗。
