"""
檔案處理器
統籌圖片轉換和 PDF 合併流程
"""

import os
from typing import List, Tuple
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
            # 1. 將檔案分組（連續的圖片為一組，PDF 單獨處理）
            # 這樣可以保持使用者定義的順序，同時允許圖片批次處理（排版）
            groups = []
            current_image_group = []
            
            for file_path in file_paths:
                if is_image_file(file_path):
                    current_image_group.append(file_path)
                else:
                    # 遇到非圖片（PDF），先結算之前的圖片組
                    if current_image_group:
                        groups.append(('images', current_image_group))
                        current_image_group = []

                    if is_pdf_file(file_path):
                        groups.append(('pdf', file_path))
                    else:
                        raise ValueError(f"不支援的檔案格式: {file_path}")
            
            # 處理最後的圖片組
            if current_image_group:
                groups.append(('images', current_image_group))
            
            # 2. 依序處理各組
            processed_count = 0
            
            for type, data in groups:
                if type == 'images':
                    # data 是圖片路徑列表
                    image_paths = data
                    count = len(image_paths)

                    if progress_callback:
                        progress_callback(processed_count, total_files, f"正在轉換 {count} 張圖片...")

                    # 使用版面選項轉換圖片
                    pdf_bytes = ImageConverter.images_to_pdf_bytes(
                        image_paths,
                        page_size=layout_options['page_size'],
                        images_per_page=layout_options['images_per_page'],
                        margin_mm=layout_options['margin_mm'],
                        spacing_mm=layout_options['spacing_mm']
                    )
                    merger.add_pdf_bytes(pdf_bytes)

                    processed_count += count
                    if progress_callback:
                        progress_callback(processed_count, total_files, f"已轉換 {count} 張圖片")

                elif type == 'pdf':
                    # data 是 PDF 檔案路徑
                    pdf_path = data
                    file_name = os.path.basename(pdf_path)

                    if progress_callback:
                        progress_callback(processed_count, total_files, f"正在合併: {file_name}")

                    merger.add_pdf(pdf_path)

                    processed_count += 1
                    if progress_callback:
                        progress_callback(processed_count, total_files, f"已合併: {file_name}")

            # 3. 儲存合併結果
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
