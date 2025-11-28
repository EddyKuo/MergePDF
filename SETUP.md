# MergePDF 設定與執行指南 (PySide6 版本)

## 📦 環境設置

### 1. 確認虛擬環境已建立
您已經建立了虛擬環境，很好！

### 2. 安裝依賴套件

在專案根目錄 `d:\code\MergePDF` 下執行：

```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 安裝所有依賴
pip install -r requirements.txt
```

或者使用 CMD：

```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 🚀 執行程式

### 方法一：使用執行腳本（推薦）

直接執行 PowerShell 腳本：

```powershell
.\run.ps1
```

### 方法二：手動執行

```powershell
# 啟動虛擬環境
.\Scripts\Activate.ps1

# 執行主程式
python main.py
```

## 📦 編譯打包

### 使用 Nuitka 編譯成執行檔

#### 簡易版（推薦）

直接執行 PowerShell 腳本：

```powershell
.\build_simple.ps1
```

這會在 `dist` 資料夾生成 `MergePDF.exe`

**注意**：PySide6 版本的編譯時間會比 tkinter 版本更長（約 15-25 分鐘）

#### 完整版（含版本資訊，如果有 icon.ico）

```powershell
.\build.ps1
```

### 手動 Nuitka 編譯指令

如果您想自訂編譯參數：

```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 最簡單的編譯方式
python -m nuitka --standalone --onefile --windows-console-mode=disable --enable-plugin=pyside6 main.py

# 進階編譯（加入更多設定）
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --enable-plugin=pyside6 ^
    --output-filename=MergePDF.exe ^
    --output-dir=dist ^
    main.py
```

## 📋 依賴套件說明

- **Pillow**: 圖片處理和資訊讀取
- **PyMuPDF** (fitz): PDF 處理、合併和圖片轉 PDF
- **PySide6**: Qt6 圖形化介面框架
- **nuitka**: Python 程式編譯器
- **ordered-set**: Nuitka 依賴

## ⚙️ Nuitka 編譯參數說明

- `--standalone`: 獨立模式，包含所有依賴
- `--onefile`: 產生單一執行檔
- `--windows-console-mode=disable`: 隱藏 console 視窗（GUI 模式）
- `--enable-plugin=pyside6`: 啟用 PySide6 支援（重要！）
- `--output-filename`: 指定輸出檔案名稱
- `--output-dir`: 指定輸出目錄

## 🔍 疑難排解

### 問題 1: 執行時出現模組找不到

**解決方式**: 確認已安裝所有依賴

```powershell
pip install -r requirements.txt
```

必要套件：
```
Pillow>=10.0.0
PyMuPDF>=1.23.0
PySide6>=6.6.0
nuitka>=2.0.0
ordered-set>=4.1.0
```

### 問題 2: Nuitka 編譯失敗

**解決方式**: 
1. 確認已安裝 C 編譯器（Windows 建議使用 MinGW-w64）
2. 嘗試更新 Nuitka：`pip install --upgrade nuitka`
3. 檢查 Python 版本（建議 3.8-3.11）
4. PySide6 編譯需要更多時間和資源，請確保有足夠的磁碟空間（至少 2GB）

### 問題 3: 編譯後的執行檔無法執行

**解決方式**:
1. 檢查是否有防毒軟體阻擋
2. 確認編譯時沒有錯誤訊息
3. 確認使用了 `--enable-plugin=pyside6` 參數
4. 嘗試使用 `--standalone` 而非 `--onefile` 模式

### 問題 4: GUI 字體或顯示異常

**解決方式**:
1. PySide6 預設使用系統字體
2. 確認 Windows 系統已更新
3. 可以在程式中自訂字體設定

## 📝 注意事項

1. **PySide6 vs tkinter**: PySide6 提供更現代化的界面，但編譯檔案較大
2. **首次編譯較慢**: Nuitka 第一次編譯 PySide6 會花較長時間（15-25分鐘），之後會快很多
3. **防毒軟體**: 編譯後的執行檔可能被防毒軟體誤判，需要加入白名單
4. **檔案大小**: 編譯後的執行檔約 50-80 MB（包含 PySide6 和所有依賴）

## 🎯 快速開始流程

```powershell
# 1. 進入專案目錄
cd d:\code\MergePDF

# 2. 安裝依賴（建議使用安裝腳本）
.\install.ps1

# 或手動安裝：
# .\Scripts\Activate.ps1
# pip install -r requirements.txt

# 3. 測試執行
.\run.ps1

# 或直接執行：
# python main.py

# 4. 編譯打包（可選）
.\build_simple.ps1
```

## 🆕 PySide6 優勢

相較於 tkinter，PySide6 提供：
- ✨ 更現代化的 UI 設計
- 🎨 更豐富的樣式自訂選項
- 📱 更好的跨平台支援
- 🔧 更強大的 Widget 功能
- 💪 更好的效能和穩定性

---

**祝使用愉快！** 如有問題請參考 README.md 或檢查錯誤訊息。
