# MergePDF - 多格式檔案合併為 PDF 工具

一個簡單易用的 Windows 桌面工具，可將多種格式檔案（JPG、PNG、PDF）合併成單一 PDF 文件。

## ✨ 功能特色

- 📁 **支援多種格式**：JPG、JPEG、PNG、PDF
- 🔄 **智慧合併**：自動將圖片轉換為 PDF 頁面，並按順序合併
- 📋 **檔案管理**：視覺化列表顯示，支援拖曳排序
- 🎯 **操作簡單**：直覺的圖形化介面，無需複雜設定
- ⚡ **高品質輸出**：保持原始圖片品質

## 🚀 快速開始

### 方法一：使用執行檔（推薦）

1. 下載 `MergePDF.exe`
2. 雙擊執行，無需安裝

### 方法二：從原始碼執行

#### 必要條件

- Python 3.8 或更高版本
- pip（Python 套件管理工具）

#### 安裝步驟

1. **下載專案**
   ```bash
   git clone <repository_url>
   cd MergePDF
   ```

2. **建立虛擬環境（建議）**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

4. **執行程式**
   ```bash
   python main.py
   ```

## 📖 使用說明

### 基本操作

1. **新增檔案**
   - 點擊「➕ 新增檔案」按鈕
   - 選擇要合併的圖片或 PDF 檔案（可多選）

2. **調整順序**
   - 在檔案列表上按右鍵
   - 選擇「🔼 上移」或「🔽 下移」調整順序
   - 或選擇「❌ 刪除」移除檔案

3. **設定輸出**
   - 輸入輸出檔案名稱（預設：`merged_output.pdf`）
   - 選擇輸出目錄（預設：桌面）

4. **執行合併**
   - 點擊「🔄 合併」按鈕
   - 等待進度完成
   - 選擇是否開啟輸出資料夾

### 支援的檔案格式

| 格式 | 副檔名 | 說明 |
|-----|-------|------|
| JPEG | `.jpg`, `.jpeg` | 常見圖片格式 |
| PNG | `.png` | 支援透明背景的圖片 |
| PDF | `.pdf` | PDF 文件 |

> **注意**：Word、Excel 等 Office 檔案請先使用「列印為 PDF」功能轉換後再合併。

## 🛠️ 技術架構

### 專案結構

```
MergePDF/
├── main.py                 # 主程式進入點
├── gui/                    # GUI 模組
│   ├── __init__.py
│   └── main_window.py     # 主視窗 (PySide6)
├── core/                   # 核心功能
│   ├── __init__.py
│   ├── image_converter.py # 圖片轉換 (PyMuPDF)
│   ├── pdf_merger.py      # PDF 合併 (PyMuPDF)
│   └── file_handler.py    # 檔案處理
├── utils/                  # 工具模組
│   ├── __init__.py
│   └── validators.py      # 驗證工具
├── requirements.txt        # 依賴清單
├── README.md              # 本文件
└── claude_project.md      # 專案規劃文件
```

### 核心依賴

- **PyMuPDF (fitz)**：PDF 處理和圖片轉 PDF
- **Pillow**：圖片資訊讀取
- **PySide6**：現代化 Qt GUI 框架
- **Nuitka**：Python 編譯器（打包用）

## 📦 打包為執行檔

本專案使用 Nuitka 進行編譯，以獲得更好的效能和更小的檔案體積。

### 使用編譯腳本（推薦）

專案內建了 PowerShell 編譯腳本，可自動處理參數設定：

```powershell
# 執行編譯腳本
.\build.ps1
```

### 手動編譯

若您希望手動執行命令：

```bash
# 安裝 Nuitka
pip install nuitka

# 執行編譯
python -m nuitka --standalone --onefile --enable-plugin=pyside6 --windows-console-mode=disable --output-filename=MergePDF.exe main.py
```

執行檔將位於 `dist` 資料夾中。

## ❓ 常見問題

### Q: 為什麼不支援 Word、Excel？
A: Word 和 Excel 本身就有「列印為 PDF」功能，您可以先將這些檔案轉換為 PDF 後再使用本工具合併。

### Q: 合併後的 PDF 可以編輯嗎？
A: 本工具產生的是標準 PDF 檔案，可使用任何 PDF 編輯軟體進行編輯。

### Q: 圖片品質會下降嗎？
A: 不會。本工具使用 img2pdf 進行轉換，能保持原始圖片品質。

### Q: 支援大量檔案合併嗎？
A: 支援，但處理時間會隨檔案數量和大小增加。建議分批合併超大型專案。

## 📝 版本歷史

- **v1.0.0** (2025-11-26)
  - 初始版本發布
  - 支援 JPG、PNG、PDF 合併
  - 圖形化介面
  - 檔案順序調整功能

## 📄 授權

本專案採用 MIT 授權條款。

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

## 📧 聯絡方式

如有問題或建議，請開啟 Issue。

---

**MergePDF** - 讓檔案合併變得簡單 ✨
