"""
檔案處理器
統籌圖片轉換和 PDF 合併流程
"""

import os
from typing import List
from core.image_converter import ImageConverter
from core.pdf_merger import PDFMerger
from utils.validators import is_image_file, is_pdf_file


class FileHandler:
    """檔案處理器，統籌整個合併流程"""
    
    @staticmethod
    def merge_files(
        file_paths: List[str], 
        output_path: str, 
        progress_callback=None,
        layout_options: dict = None
    ) -> None:
        """
        合併多個檔案（圖片和 PDF）為單一 PDF
        
        Args:
            file_paths: 要合併的檔案路徑列表（按順序）
            output_path: 輸出 PDF 檔案路徑
            progress_callback: 進度回呼函數 (可選)，接收參數 (current, total, message)
            layout_options: 圖片版面選項 (可選)
                - page_size: (寬, 高) mm 或 None
                - images_per_page: (列, 欄)
                - margin_mm: 邊距
                - spacing_mm: 間距
        """
        if not file_paths:
            raise ValueError("檔案列表不能為空")
        
        # 預設版面選項
        if layout_options is None:
            layout_options = {
                'page_size': None,
                'images_per_page': (1, 1),
                'margin_mm': 0,
                'spacing_mm': 0
            }
        
        total_files = len(file_paths)
        merger = PDFMerger()
        
        try:
            # 分離圖片和 PDF
            image_files = []
            pdf_files_positions = []
            
            for index, file_path in enumerate(file_paths):
                if is_image_file(file_path):
                    image_files.append((index, file_path))
                elif is_pdf_file(file_path):
                    pdf_files_positions.append((index, file_path))
                else:
                    raise ValueError(f"不supported的檔案格式: {file_path}")
            
            # 處理圖片檔案（批次轉換）
            if image_files:
                # 取得圖片路徑列表
                img_paths = [path for _, path in image_files]
                
                # 使用版面選項轉換圖片
                pdf_bytes = ImageConverter.images_to_pdf_bytes(
                    img_paths,
                    page_size=layout_options['page_size'],
                    images_per_page=layout_options['images_per_page'],
                    margin_mm=layout_options['margin_mm'],
                    spacing_mm=layout_options['spacing_mm']
                )
                merger.add_pdf_bytes(pdf_bytes)
                
                if progress_callback:
                    progress_callback(len(image_files), total_files, f"已轉換 {len(image_files)} 張圖片")
            
            # 處理 PDF 檔案
            for index, pdf_path in pdf_files_positions:
                file_name = os.path.basename(pdf_path)
                merger.add_pdf(pdf_path)
                
                if progress_callback:
                    progress_callback(index + 1, total_files, f"處理中: {file_name}")
            
            # 儲存合併結果
            if progress_callback:
                progress_callback(total_files, total_files, "正在儲存...")
            
            merger.save(output_path)
            
            if progress_callback:
                progress_callback(total_files, total_files, "完成！")
                
        except Exception as e:
            raise Exception(f"合併檔案失敗: {str(e)}")
        finally:
            merger.close()
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        取得檔案資訊
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            dict: 檔案資訊
        """
        info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': os.path.getsize(file_path),
            'type': 'Unknown'
        }
        
        try:
            if is_image_file(file_path):
                info['type'] = 'Image'
                img_info = ImageConverter.get_image_info(file_path)
                info.update(img_info)
            elif is_pdf_file(file_path):
                info['type'] = 'PDF'
                pdf_info = PDFMerger.get_pdf_info(file_path)
                info.update(pdf_info)
        except Exception as e:
            info['error'] = str(e)
        
        return info
