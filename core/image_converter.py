"""
圖片轉換模組
使用 PyMuPDF (fitz) 將 JPG/PNG 圖片轉換為 PDF 格式
支援多圖併頁和版面設定
"""

import fitz  # PyMuPDF
from PIL import Image
from typing import List, Tuple, Optional
import io
import os


class ImageConverter:
    """圖片轉 PDF 轉換器（使用 PyMuPDF）"""
    
    # 常用頁面大小 (寬, 高) 單位: 點 (1mm = 2.83465 points)
    PAGE_SIZES = {
        'A4': (595, 842),      # 210mm × 297mm
        'LETTER': (612, 792),  # 216mm × 279mm
        'A3': (842, 1191),     # 297mm × 420mm
    }
    
    @staticmethod
    def mm_to_points(mm: float) -> float:
        """將毫米轉換為點"""
        return mm * 2.83465
    
    @staticmethod
    def image_to_pdf_bytes(
        image_path: str,
        page_size: Optional[Tuple[int, int]] = None,
        margin_mm: float = 0
    ) -> bytes:
        """
        將單張圖片轉換為 PDF 格式的位元組資料
        
        Args:
            image_path: 圖片檔案路徑
            page_size: 頁面大小 (寬, 高) mm，None 表示使用原始大小
            margin_mm: 頁面邊距 (毫米)
            
        Returns:
            bytes: PDF 格式的位元組資料
        """
        try:
            pdf_document = fitz.open()
            
            # 開啟圖片以獲取尺寸
            img = Image.open(image_path)
            img_width, img_height = img.size
            img.close()
            
            # 計算頁面大小
            if page_size:
                page_w = ImageConverter.mm_to_points(page_size[0])
                page_h = ImageConverter.mm_to_points(page_size[1])
            else:
                page_w, page_h = img_width, img_height
            
            # 計算邊距
            margin = ImageConverter.mm_to_points(margin_mm)
            
            # 創建頁面
            page = pdf_document.new_page(width=page_w, height=page_h)
            
            # 計算圖片放置區域
            img_rect = fitz.Rect(margin, margin, page_w - margin, page_h - margin)
            
            # 插入圖片（自動縮放以適應矩形）
            page.insert_image(img_rect, filename=image_path, keep_proportion=True)
            
            pdf_bytes = pdf_document.tobytes()
            pdf_document.close()
            
            return pdf_bytes
            
        except Exception as e:
            raise Exception(f"圖片轉換失敗 ({image_path}): {str(e)}")
    
    @staticmethod
    def images_to_pdf_bytes(
        image_paths: List[str],
        page_size: Optional[Tuple[int, int]] = None,
        images_per_page: Tuple[int, int] = (1, 1),
        margin_mm: float = 10,
        spacing_mm: float = 5
    ) -> bytes:
        """
        將多張圖片轉換為 PDF，支援多圖併頁
        
        Args:
            image_paths: 圖片檔案路徑列表
            page_size: 頁面大小 (寬, 高) mm，None 表示使用原始大小
            images_per_page: 每頁圖片數 (列數, 欄數)
            margin_mm: 頁面邊距 (毫米)
            spacing_mm: 圖片間距 (毫米)
            
        Returns:
            bytes: PDF 格式的位元組資料
        """
        try:
            pdf_document = fitz.open()
            
            rows, cols = images_per_page
            images_count = rows * cols
            
            # 將圖片分組
            for i in range(0, len(image_paths), images_count):
                batch = image_paths[i:i + images_count]
                
                # 確定頁面大小
                if page_size:
                    page_w = ImageConverter.mm_to_points(page_size[0])
                    page_h = ImageConverter.mm_to_points(page_size[1])
                else:
                    # 使用第一張圖片的大小
                    img = Image.open(batch[0])
                    page_w, page_h = img.size
                    img.close()
                
                # 創建新頁面
                page = pdf_document.new_page(width=page_w, height=page_h)
                
                # 計算邊距和間距
                margin = ImageConverter.mm_to_points(margin_mm)
                spacing = ImageConverter.mm_to_points(spacing_mm)
                
                # 計算可用區域
                available_w = page_w - 2 * margin - (cols - 1) * spacing
                available_h = page_h - 2 * margin - (rows - 1) * spacing
                
                # 每個格子的大小
                cell_w = available_w / cols
                cell_h = available_h / rows
                
                # 放置圖片
                for idx, img_path in enumerate(batch):
                    row = idx // cols
                    col = idx % cols
                    
                    # 計算圖片位置
                    x = margin + col * (cell_w + spacing)
                    y = margin + row * (cell_h + spacing)
                    
                    img_rect = fitz.Rect(x, y, x + cell_w, y + cell_h)
                    
                    # 插入圖片
                    page.insert_image(img_rect, filename=img_path, keep_proportion=True)
            
            pdf_bytes = pdf_document.tobytes()
            pdf_document.close()
            
            return pdf_bytes
            
        except Exception as e:
            raise Exception(f"多圖片轉換失敗: {str(e)}")
    
    @staticmethod
    def save_image_as_pdf(image_path: str, output_path: str) -> None:
        """
        將圖片直接儲存為 PDF 檔案
        
        Args:
            image_path: 圖片檔案路徑
            output_path: 輸出 PDF 檔案路徑
        """
        try:
            pdf_bytes = ImageConverter.image_to_pdf_bytes(image_path)
            with open(output_path, 'wb') as output_file:
                output_file.write(pdf_bytes)
        except Exception as e:
            raise Exception(f"儲存 PDF 失敗: {str(e)}")
    
    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """
        取得圖片資訊
        
        Args:
            image_path: 圖片檔案路徑
            
        Returns:
            dict: 包含寬度、高度、格式等資訊
        """
        try:
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode
                }
        except Exception as e:
            raise Exception(f"讀取圖片資訊失敗: {str(e)}")
