"""
主視窗 GUI - 使用 PySide6 (Qt)
MergePDF 應用程式的主要使用者介面
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QMessageBox, QLabel, QLineEdit, QProgressDialog, QHeaderView,
    QMenu, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
import os
from typing import List, Optional
from core.file_handler import FileHandler
from utils.validators import validate_files, get_file_type


class MainWindow(QMainWindow):
    """主視窗類別 - 使用 PySide6"""
    
    def __init__(self):
        """初始化主視窗"""
        super().__init__()
        self.file_list: List[str] = []
        self.dark_mode = False  # 預設為亮色主題
        self.init_ui()
        
        # 設定預設輸出路徑為桌面
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_dir_input.setText(desktop)
    
    def init_ui(self):
        """初始化使用者介面"""
        self.setWindowTitle("MergePDF - 檔案合併工具")
        self.setGeometry(100, 100, 900, 650)
        self.setMinimumSize(QSize(800, 600))
        
        # 建立中央 widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主要佈局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # ===== 頂部工具列 =====
        toolbar_layout = QHBoxLayout()
        
        # 主題切換按鈕
        self.theme_btn = QPushButton("🌓 切換主題")
        self.theme_btn.setMinimumHeight(40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        toolbar_layout.addWidget(self.theme_btn)
        
        # 新增檔案按鈕
        self.add_btn = QPushButton("➕ 新增檔案")
        self.add_btn.setMinimumHeight(40)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.add_btn.clicked.connect(self.add_files)
        toolbar_layout.addWidget(self.add_btn)
        
        # 清空按鈕
        self.clear_btn = QPushButton("🗑️ 清空列表")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_all)
        toolbar_layout.addWidget(self.clear_btn)
        
        toolbar_layout.addStretch()
        
        # 合併按鈕
        self.merge_btn = QPushButton("🔄 合併")
        self.merge_btn.setMinimumHeight(40)
        self.merge_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                font-weight: bold;
                font-size: 12pt;
                border: none;
                border-radius: 6px;
                padding: 8px 30px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        self.merge_btn.clicked.connect(self.merge_files)
        toolbar_layout.addWidget(self.merge_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # ===== 檔案列表 =====
        list_label = QLabel("📁 檔案列表（可拖曳調整順序）")
        list_label.setObjectName("list_label")
        list_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #007bff; padding: 5px;")
        main_layout.addWidget(list_label)
        
        # 建立表格
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(4)
        self.file_table.setHorizontalHeaderLabels(["序號", "檔案名稱", "類型", "完整路徑"])
        
        # 設定表格樣式 - 明亮色系
        self.file_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: #ffffff;
                gridline-color: #e9ecef;
                alternate-background-color: #f8f9fa;
                selection-background-color: #007bff;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e9ecef;
                color: #212529;
            }
            QTableWidget::item:hover {
                background-color: #e7f3ff;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }
            QTableWidget::item:selected:hover {
                background-color: #0056b3;
                color: white;
                font-weight: bold;
            }
            QTableWidget::item:focus {
                outline: 2px solid #007bff;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 12px;
                border: none;
                border-right: 1px solid #0056b3;
                font-weight: bold;
                font-size: 10pt;
            }
            QHeaderView::section:first {
                border-top-left-radius: 6px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 6px;
                border-right: none;
            }
        """)
        
        # 啟用交替行顏色
        self.file_table.setAlternatingRowColors(True)
        
        # 啟用拖放功能
        self.file_table.setDragEnabled(True)
        self.file_table.setAcceptDrops(True)
        self.file_table.setDragDropMode(QTableWidget.DragDropMode.InternalMove)
        self.file_table.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.file_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # 設定欄位寬度
        header = self.file_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.file_table.setColumnWidth(0, 60)
        self.file_table.setColumnWidth(2, 80)
        
        # 啟用選取整列
        self.file_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.file_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # 覆寫 dropEvent 來處理拖放
        def custom_drop_event(event):
            """自訂拖放事件處理"""
            if event.source() == self.file_table:
                # 取得拖放的來源和目標行
                source_row = self.file_table.currentRow()
                drop_pos = event.position().toPoint() if hasattr(event.position(), 'toPoint') else event.pos()
                target_row = self.file_table.indexAt(drop_pos).row()
                
                # 如果目標行無效（拖到空白處），使用最後一行
                if target_row < 0:
                    target_row = len(self.file_list) - 1
                
                if source_row >= 0 and target_row >= 0 and source_row != target_row:
                    # 更新內部檔案列表
                    moved_file = self.file_list.pop(source_row)
                    self.file_list.insert(target_row, moved_file)
                    
                    # 重新整理表格
                    self.update_file_table()
                    
                    # 選取移動後的行
                    self.file_table.setCurrentCell(target_row, 0)
                    
                    self.statusBar().showMessage(f"✨ 已移動檔案至位置 {target_row + 1}")
                
                # 阻止預設行為（防止刪除項目）
                event.setDropAction(Qt.DropAction.IgnoreAction)
                event.accept()
            else:
                event.ignore()
        
        self.file_table.dropEvent = custom_drop_event
        
        main_layout.addWidget(self.file_table)
        
        # ===== 輸出設定 =====
        output_label = QLabel("⚙️ 輸出設定")
        output_label.setObjectName("output_label")
        output_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #28a745; padding: 5px;")
        main_layout.addWidget(output_label)
        
        # 檔案名稱
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("輸出檔名:"))
        self.output_name_input = QLineEdit("merged_output.pdf")
        self.output_name_input.setMinimumHeight(30)
        name_layout.addWidget(self.output_name_input)
        main_layout.addLayout(name_layout)
        
        # 輸出目錄
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("輸出路徑:"))
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setMinimumHeight(30)
        dir_layout.addWidget(self.output_dir_input)
        
        browse_btn = QPushButton("瀏覽...")
        browse_btn.setMinimumHeight(30)
        browse_btn.clicked.connect(self.browse_output_dir)
        dir_layout.addWidget(browse_btn)
        main_layout.addLayout(dir_layout)
        
        # ===== 圖片版面設定 =====
        layout_label = QLabel("🖼️ 圖片版面設定")
        layout_label.setObjectName("layout_label")
        layout_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #fd7e14; padding: 5px;")
        main_layout.addWidget(layout_label)
        
        # 版面設定區域
        layout_settings_frame = QWidget()
        layout_settings_layout = QVBoxLayout(layout_settings_frame)
        layout_settings_layout.setContentsMargins(10, 5, 10, 5)
        
        # 第一行：頁面大小和每頁圖片數
        row1_layout = QHBoxLayout()
        
        # 頁面大小
        row1_layout.addWidget(QLabel("頁面大小:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4 (210×297mm)", "Letter (216×279mm)", "A3 (297×420mm)", "原始大小"])
        self.page_size_combo.setMinimumHeight(30)
        row1_layout.addWidget(self.page_size_combo)
        
        row1_layout.addSpacing(20)
        
        # 每頁圖片數量
        row1_layout.addWidget(QLabel("每頁圖片數:"))
        self.images_per_page_combo = QComboBox()
        self.images_per_page_combo.addItems(["1 張 (全頁)", "2 張 (橫排)", "4 張 (2×2)", "6 張 (2×3)", "9 張 (3×3)"])
        self.images_per_page_combo.setMinimumHeight(30)
        row1_layout.addWidget(self.images_per_page_combo)
        
        row1_layout.addStretch()
        layout_settings_layout.addLayout(row1_layout)
        
        # 第二行：邊距設定
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(QLabel("頁面邊距:"))
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 50)
        self.margin_spin.setValue(10)
        self.margin_spin.setSuffix(" mm")
        self.margin_spin.setMinimumHeight(30)
        row2_layout.addWidget(self.margin_spin)
        
        row2_layout.addSpacing(20)
        row2_layout.addWidget(QLabel("圖片間距:"))
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setRange(0, 30)
        self.spacing_spin.setValue(5)
        self.spacing_spin.setSuffix(" mm")
        self.spacing_spin.setMinimumHeight(30)
        row2_layout.addWidget(self.spacing_spin)
        
        row2_layout.addStretch()
        layout_settings_layout.addLayout(row2_layout)
        
        main_layout.addWidget(layout_settings_frame)
        
        # ===== 狀態列 =====
        self.statusBar().showMessage("✨ 就緒")
        
        # 應用預設主題
        self.apply_theme()
    
    def toggle_theme(self):
        """切換亮暗主題"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        theme_name = "暗色" if self.dark_mode else "亮色"
        self.statusBar().showMessage(f"🎨 已切換至{theme_name}主題")
    
    def apply_theme(self):
        """應用主題配色"""
        if self.dark_mode:
            # ===== 暗色主題 =====
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    background-color: #2b2b2b;
                    color: #e0e0e0;
                }
                QLabel {
                    color: #e0e0e0;
                }
                QLineEdit {
                    background-color: #3c3c3c;
                    border: 2px solid #555555;
                    border-radius: 4px;
                    padding: 5px;
                    color: #e0e0e0;
                }
                QLineEdit:focus {
                    border: 2px solid #4a9eff;
                }
            """)
            
            # 更新按鈕樣式
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d7d46;
                    color: white;
                    font-weight: bold;
                    font-size: 11pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #3a9b5c;
                }
                QPushButton:pressed {
                    background-color: #256838;
                }
            """)
            
            self.clear_btn.setStyleSheet("""
                QPushButton {
                    background-color: #c93a3a;
                    color: white;
                    font-weight: bold;
                    font-size: 11pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #e04545;
                }
                QPushButton:pressed {
                    background-color: #b03030;
                }
            """)
            
            self.merge_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3a7bc8;
                    color: white;
                    font-weight: bold;
                    font-size: 12pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 30px;
                }
                QPushButton:hover {
                    background-color: #4a8dd8;
                }
                QPushButton:pressed {
                    background-color: #2a6bb8;
                }
            """)
            
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    font-weight: bold;
                    font-size: 10pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 15px;
                }
                QPushButton:hover {
                    background-color: #7d8a94;
                }
                QPushButton:pressed {
                    background-color: #5c656d;
                }
            """)
            
            # 更新表格樣式
            self.file_table.setStyleSheet("""
                QTableWidget {
                    border: 2px solid #3c3c3c;
                    border-radius: 8px;
                    background-color: #2b2b2b;
                    gridline-color: #3c3c3c;
                    alternate-background-color: #353535;
                    selection-background-color: #0d6efd;
                    selection-color: white;
                }
                QTableWidget::item {
                    padding: 10px;
                    border-bottom: 1px solid #3c3c3c;
                    color: #e0e0e0;
                }
                QTableWidget::item:hover {
                    background-color: #3c4a57;
                }
                QTableWidget::item:selected {
                    background-color: #0d6efd;
                    color: white;
                    font-weight: bold;
                }
                QTableWidget::item:selected:hover {
                    background-color: #0a58ca;
                    color: white;
                    font-weight: bold;
                }
                QTableWidget::item:focus {
                    outline: 2px solid #4a9eff;
                }
                QHeaderView::section {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    padding: 12px;
                    border: none;
                    border-right: 1px solid #2b2b2b;
                    font-weight: bold;
                    font-size: 10pt;
                }
                QHeaderView::section:first {
                    border-top-left-radius: 6px;
                }
                QHeaderView::section:last {
                    border-top-right-radius: 6px;
                    border-right: none;
                }
            """)
            
            # 更新標籤樣式
            self.findChild(QLabel, "list_label").setStyleSheet(
                "font-size: 12pt; font-weight: bold; color: #4a9eff; padding: 5px;"
            )
            self.findChild(QLabel, "output_label").setStyleSheet(
                "font-size: 12pt; font-weight: bold; color: #3a9b5c; padding: 5px;"
            )
            layout_label = self.findChild(QLabel, "layout_label")
            if layout_label:
                layout_label.setStyleSheet(
                    "font-size: 12pt; font-weight: bold; color: #fd8c3a; padding: 5px;"
                )
            
            # 更新狀態列
            self.statusBar().setStyleSheet("""
                QStatusBar { 
                    background-color: #1a1a1a; 
                    color: #e0e0e0;
                    border-top: 2px solid #3c3c3c;
                    font-weight: bold;
                }
            """)
            
        else:
            # ===== 亮色主題 =====
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f8f9fa;
                }
                QWidget {
                    background-color: #ffffff;
                    color: #212529;
                }
                QLabel {
                    color: #212529;
                }
                QLineEdit {
                    background-color: #ffffff;
                    border: 2px solid #dee2e6;
                    border-radius: 4px;
                    padding: 5px;
                    color: #212529;
                }
                QLineEdit:focus {
                    border: 2px solid #4CAF50;
                }
            """)
            
            # 更新按鈕樣式
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    font-size: 11pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
                QPushButton:pressed {
                    background-color: #1e7e34;
                }
            """)
            
            self.clear_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    font-weight: bold;
                    font-size: 11pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            
            self.merge_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    font-weight: bold;
                    font-size: 12pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 30px;
                }
                QPushButton:hover {
                    background-color: #0069d9;
                }
                QPushButton:pressed {
                    background-color: #0056b3;
                }
            """)
            
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    font-weight: bold;
                    font-size: 10pt;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 15px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
                QPushButton:pressed {
                    background-color: #545b62;
                }
            """)
            
            # 更新表格樣式
            self.file_table.setStyleSheet("""
                QTableWidget {
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    background-color: #ffffff;
                    gridline-color: #e9ecef;
                    alternate-background-color: #f8f9fa;
                    selection-background-color: #007bff;
                    selection-color: white;
                }
                QTableWidget::item {
                    padding: 10px;
                    border-bottom: 1px solid #e9ecef;
                    color: #212529;
                }
                QTableWidget::item:hover {
                    background-color: #e7f3ff;
                }
                QTableWidget::item:selected {
                    background-color: #007bff;
                    color: white;
                    font-weight: bold;
                }
                QTableWidget::item:selected:hover {
                    background-color: #0056b3;
                    color: white;
                    font-weight: bold;
                }
                QTableWidget::item:focus {
                    outline: 2px solid #007bff;
                }
                QHeaderView::section {
                    background-color: #007bff;
                    color: white;
                    padding: 12px;
                    border: none;
                    border-right: 1px solid #0056b3;
                    font-weight: bold;
                    font-size: 10pt;
                }
                QHeaderView::section:first {
                    border-top-left-radius: 6px;
                }
                QHeaderView::section:last {
                    border-top-right-radius: 6px;
                    border-right: none;
                }
            """)
            
            # 更新標籤樣式
            self.findChild(QLabel, "list_label").setStyleSheet(
                "font-size: 12pt; font-weight: bold; color: #007bff; padding: 5px;"
            )
            self.findChild(QLabel, "output_label").setStyleSheet(
                "font-size: 12pt; font-weight: bold; color: #28a745; padding: 5px;"
            )
            layout_label = self.findChild(QLabel, "layout_label")
            if layout_label:
                layout_label.setStyleSheet(
                    "font-size: 12pt; font-weight: bold; color: #fd7e14; padding: 5px;"
                )
            
            # 更新狀態列
            self.statusBar().setStyleSheet("""
                QStatusBar { 
                    background-color: #e7f3ff; 
                    color: #212529;
                    border-top: 2px solid #007bff;
                    font-weight: bold;
                }
            """)
    
    def add_files(self):
        """新增檔案到列表"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "選擇要合併的檔案",
            "",
            "所有支援格式 (*.jpg *.jpeg *.png *.pdf);;圖片檔案 (*.jpg *.jpeg *.png);;PDF 檔案 (*.pdf);;所有檔案 (*.*)"
        )
        
        if file_paths:
            valid_files, invalid_files = validate_files(file_paths)
            
            # 加入有效檔案
            self.file_list.extend(valid_files)
            self.update_file_table()
            
            # 提示無效檔案
            if invalid_files:
                QMessageBox.warning(
                    self,
                    "部分檔案無效",
                    f"以下檔案格式不支援，已忽略：\n\n" + "\n".join([os.path.basename(f) for f in invalid_files])
                )
            
            self.statusBar().showMessage(f"已新增 {len(valid_files)} 個檔案")
    
    def clear_all(self):
        """清空所有檔案"""
        if self.file_list:
            reply = QMessageBox.question(
                self,
                "確認",
                "確定要清空所有檔案嗎？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.file_list.clear()
                self.update_file_table()
                self.statusBar().showMessage("已清空列表")
    
    def update_file_table(self):
        """更新檔案列表顯示"""
        self.file_table.setRowCount(len(self.file_list))
        
        for index, file_path in enumerate(self.file_list):
            # 序號
            self.file_table.setItem(index, 0, QTableWidgetItem(str(index + 1)))
            
            # 檔案名稱
            file_name = os.path.basename(file_path)
            self.file_table.setItem(index, 1, QTableWidgetItem(file_name))
            
            # 類型
            file_type = get_file_type(file_path)
            self.file_table.setItem(index, 2, QTableWidgetItem(file_type))
            
            # 完整路徑
            self.file_table.setItem(index, 3, QTableWidgetItem(file_path))
        
        # 更新狀態列
        self.statusBar().showMessage(f"共 {len(self.file_list)} 個檔案")
    
    def show_context_menu(self, position):
        """顯示右鍵選單"""
        if self.file_table.currentRow() >= 0:
            menu = QMenu()
            
            move_up_action = QAction("🔼 上移", self)
            move_up_action.triggered.connect(self.move_up)
            menu.addAction(move_up_action)
            
            move_down_action = QAction("🔽 下移", self)
            move_down_action.triggered.connect(self.move_down)
            menu.addAction(move_down_action)
            
            menu.addSeparator()
            
            remove_action = QAction("❌ 刪除", self)
            remove_action.triggered.connect(self.remove_selected)
            menu.addAction(remove_action)
            
            menu.exec(self.file_table.viewport().mapToGlobal(position))
    
    def move_up(self):
        """上移選取的檔案"""
        current_row = self.file_table.currentRow()
        if current_row > 0:
            self.file_list[current_row], self.file_list[current_row - 1] = \
                self.file_list[current_row - 1], self.file_list[current_row]
            self.update_file_table()
            self.file_table.setCurrentCell(current_row - 1, 0)
    
    def move_down(self):
        """下移選取的檔案"""
        current_row = self.file_table.currentRow()
        if current_row < len(self.file_list) - 1:
            self.file_list[current_row], self.file_list[current_row + 1] = \
                self.file_list[current_row + 1], self.file_list[current_row]
            self.update_file_table()
            self.file_table.setCurrentCell(current_row + 1, 0)
    
    def remove_selected(self):
        """刪除選取的檔案"""
        current_row = self.file_table.currentRow()
        if current_row >= 0:
            del self.file_list[current_row]
            self.update_file_table()
            self.statusBar().showMessage("已刪除檔案")
    
    def browse_output_dir(self):
        """瀏覽輸出目錄"""
        directory = QFileDialog.getExistingDirectory(self, "選擇輸出目錄")
        if directory:
            self.output_dir_input.setText(directory)
    
    def merge_files(self):
        """執行合併"""
        # 驗證檔案列表
        if not self.file_list:
            QMessageBox.warning(self, "無法合併", "請先新增要合併的檔案！")
            return
        
        # 驗證輸出設定
        output_name = self.output_name_input.text().strip()
        if not output_name:
            QMessageBox.warning(self, "無法合併", "請輸入輸出檔案名稱！")
            return
        
        # 確保副檔名為 .pdf
        if not output_name.lower().endswith('.pdf'):
            output_name += '.pdf'
        
        output_dir = self.output_dir_input.text().strip()
        if not output_dir or not os.path.isdir(output_dir):
            QMessageBox.warning(self, "無法合併", "請選擇有效的輸出目錄！")
            return
        
        output_path = os.path.join(output_dir, output_name)
        
        # 確認覆蓋
        if os.path.exists(output_path):
            reply = QMessageBox.question(
                self,
                "確認覆蓋",
                f"檔案已存在：\n{output_path}\n\n是否要覆蓋？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # 建立進度對話框
        progress = QProgressDialog("正在合併檔案，請稍候...", "取消", 0, len(self.file_list), self)
        progress.setWindowTitle("合併中")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        
        def progress_callback(current, total, message):
            """進度回呼函數"""
            progress.setValue(current)
            progress.setLabelText(f"進度: {current}/{total}\n{message}")
            if progress.wasCanceled():
                raise Exception("使用者取消操作")
        
        # 執行合併
        try:
            # 取得圖片版面設定
            layout_options = self._get_layout_options()
            
            FileHandler.merge_files(
                self.file_list, 
                output_path, 
                progress_callback,
                layout_options=layout_options
            )
            progress.close()
            
            # 成功提示
            reply = QMessageBox.question(
                self,
                "合併完成",
                f"檔案已成功合併！\n\n輸出位置：\n{output_path}\n\n是否要開啟檔案所在資料夾？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                os.startfile(output_dir)
            
            self.statusBar().showMessage("合併完成！")
            
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "合併失敗", f"合併過程發生錯誤：\n\n{str(e)}")
            self.statusBar().showMessage("合併失敗")
    
    def _get_layout_options(self) -> dict:
        """取得圖片版面設定選項"""
        # 頁面大小映射 (寬, 高) mm
        page_sizes = {
            0: (210, 297),   # A4
            1: (216, 279),   # Letter
            2: (297, 420),   # A3
            3: None          # 原始大小
        }
        
        # 每頁圖片數映射 (列, 欄)
        images_per_page = {
            0: (1, 1),   # 1張
            1: (1, 2),   # 2張橫排
            2: (2, 2),   # 4張
            3: (2, 3),   # 6張
            4: (3, 3)    # 9張
        }
        
        return {
            'page_size': page_sizes[self.page_size_combo.currentIndex()],
            'images_per_page': images_per_page[self.images_per_page_combo.currentIndex()],
            'margin_mm': self.margin_spin.value(),
            'spacing_mm': self.spacing_spin.value()
        }


def create_app():
    """建立並返回主視窗"""
    return MainWindow()
