"""
PDF 合併模組
使用 PyMuPDF (fitz) 合併多個 PDF 檔案
"""

import fitz  # PyMuPDF
from typing import List
import os


class PDFMerger:
    """PDF 合併器（使用 PyMuPDF）"""
    
    def __init__(self):
        """初始化 PDF 合併器"""
        self.pdf_documents = []
        self.temp_docs = []  # 儲存暫時的 PDF 文件物件
    
    def add_pdf(self, pdf_path: str) -> None:
        """
        加入 PDF 檔案到合併列表
        
        Args:
            pdf_path: PDF 檔案路徑
            
        Raises:
            Exception: 加入失敗時拋出異常
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"檔案不存在: {pdf_path}")
            
            # 開啟 PDF 文件並加入列表
            doc = fitz.open(pdf_path)
            self.pdf_documents.append(doc)
            
        except Exception as e:
            raise Exception(f"加入 PDF 失敗 ({pdf_path}): {str(e)}")
    
    def add_pdf_bytes(self, pdf_bytes: bytes) -> None:
        """
        加入 PDF 位元組資料到合併列表
        
        Args:
            pdf_bytes: PDF 格式的位元組資料
            
        Raises:
            Exception: 加入失敗時拋出異常
        """
        try:
            # 從位元組資料建立 PDF 文件
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            self.pdf_documents.append(doc)
            self.temp_docs.append(doc)  # 記錄為暫時文件
            
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
            if not self.pdf_documents:
                raise ValueError("沒有要合併的 PDF 文件")
            
            # 建立新的 PDF 文件
            result = fitz.open()
            
            # 合併所有 PDF
            for doc in self.pdf_documents:
                result.insert_pdf(doc)
            
            # 儲存結果
            result.save(output_path)
            result.close()
            
        except Exception as e:
            raise Exception(f"儲存合併 PDF 失敗: {str(e)}")
        finally:
            self.close()
    
    def close(self) -> None:
        """關閉合併器，釋放資源"""
        for doc in self.pdf_documents:
            try:
                doc.close()
            except:
                pass
        self.pdf_documents.clear()
        self.temp_docs.clear()
    
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
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            page_count = doc.page_count
            doc.close()
            
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
            raise Exception(f"合併 PDF 失敗: {str(e)}")
        finally:
            merger.close()
