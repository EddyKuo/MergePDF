"""
PDF 合併模組
使用 PyMuPDF (fitz) 合併多個 PDF 檔案
"""

import fitz  # PyMuPDF
from typing import List, Union
import os


class PDFMerger:
    """PDF 合併器（使用 PyMuPDF）"""
    
    def __init__(self):
        """初始化 PDF 合併器"""
        self.result_doc = fitz.open()
    
    def add_pdf(self, pdf_path: str) -> None:
        """
        加入 PDF 檔案並合併
        
        Args:
            pdf_path: PDF 檔案路徑
            
        Raises:
            Exception: 加入失敗時拋出異常
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"檔案不存在: {pdf_path}")
            
            # 開啟 PDF 文件並合併
            with fitz.open(pdf_path) as doc:
                self.result_doc.insert_pdf(doc)
            
        except Exception as e:
            raise Exception(f"加入 PDF 失敗 ({pdf_path}): {str(e)}")
    
    def add_pdf_bytes(self, pdf_bytes: bytes) -> None:
        """
        加入 PDF 位元組資料並合併
        
        Args:
            pdf_bytes: PDF 格式的位元組資料
            
        Raises:
            Exception: 加入失敗時拋出異常
        """
        try:
            # 從位元組資料建立 PDF 文件
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                self.result_doc.insert_pdf(doc)
            
        except Exception as e:
            raise Exception(f"加入 PDF 位元組資料失敗: {str(e)}")
    
    def save(self, output_path: str) -> None:
        """
        儲存合併後的 PDF 檔案
        
        Args:
            output_path: 輸出檔案路徑
            
        Raises:
            Exception: 儲存失敗時拋出異常
        """
        try:
            if self.result_doc.page_count == 0:
                raise ValueError("沒有要合併的頁面")
            
            # 儲存結果
            self.result_doc.save(output_path)
            
        except Exception as e:
            raise Exception(f"儲存合併 PDF 失敗: {str(e)}")
        finally:
            self.close()
    
    def close(self) -> None:
        """關閉合併器，釋放資源"""
        try:
            if self.result_doc:
                self.result_doc.close()
                self.result_doc = None
        except:
            pass
    
    @staticmethod
    def get_pdf_info(pdf_path: str) -> dict:
        """
        取得 PDF 檔案資訊
        
        Args:
            pdf_path: PDF 檔案路徑
            
        Returns:
            dict: 包含頁數、作者等資訊
        """
        try:
            with fitz.open(pdf_path) as doc:
                metadata = doc.metadata
                page_count = doc.page_count

                return {
                    'pages': page_count,
                    'metadata': metadata,
                    'title': metadata.get('title', ''),
                    'author': metadata.get('author', ''),
                    'subject': metadata.get('subject', '')
                }
        except Exception as e:
            raise Exception(f"讀取 PDF 資訊失敗: {str(e)}")
    
    @staticmethod
    def merge_pdfs(pdf_paths: List[str], output_path: str) -> None:
        """
        快速合併多個 PDF 檔案（靜態方法）
        
        Args:
            pdf_paths: PDF 檔案路徑列表
            output_path: 輸出檔案路徑
            
        Raises:
            Exception: 合併失敗時拋出異常
        """
        merger = PDFMerger()
        try:
            for pdf_path in pdf_paths:
                merger.add_pdf(pdf_path)
            merger.save(output_path)
        except Exception as e:
            if merger.result_doc:
                merger.close()
            raise Exception(f"合併 PDF 失敗: {str(e)}")
