"""
MergePDF - 多格式檔案合併為 PDF 工具
主程式進入點 - 使用 PySide6
"""

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from gui.main_window import create_app


def main():
    """主函數"""
    try:
        # 建立 Qt 應用程式
        app = QApplication(sys.argv)
        app.setApplicationName("MergePDF")
        app.setOrganizationName("MergePDF")
        
        # 設定應用程式樣式
        app.setStyle("Fusion")
        
        # 建立並顯示主視窗
        main_window = create_app()
        main_window.show()
        
        # 執行應用程式主迴圈
        sys.exit(app.exec())
        
    except Exception as e:
        # 錯誤處理
        import traceback
        error_msg = f"程式發生錯誤：\n\n{str(e)}\n\n{traceback.format_exc()}"
        
        # 嘗試顯示錯誤對話框
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            QMessageBox.critical(None, "程式錯誤", error_msg)
        except:
            # 如果 GUI 失敗，輸出到 console
            print(error_msg, file=sys.stderr)
        
        sys.exit(1)


if __name__ == "__main__":
    main()
