"""
檔案驗證工具
用於檢查檔案格式和有效性
"""

import os
from typing import List, Tuple

# 支援的檔案格式
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png'}
SUPPORTED_PDF_FORMAT = {'.pdf'}
SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS | SUPPORTED_PDF_FORMAT


def is_supported_file(file_path: str) -> bool:
    """
    檢查檔案是否為支援的格式
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        bool: 是否為支援的格式
    """
    if not os.path.exists(file_path):
        return False
    
    if not os.path.isfile(file_path):
        return False
    
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_FORMATS


def is_image_file(file_path: str) -> bool:
    """
    檢查檔案是否為圖片格式
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        bool: 是否為圖片格式
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_IMAGE_FORMATS


def is_pdf_file(file_path: str) -> bool:
    """
    檢查檔案是否為 PDF 格式
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        bool: 是否為 PDF 格式
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_PDF_FORMAT


def validate_files(file_paths: List[str]) -> Tuple[List[str], List[str]]:
    """
    驗證檔案列表，分離有效和無效的檔案
    
    Args:
        file_paths: 檔案路徑列表
        
    Returns:
        Tuple[List[str], List[str]]: (有效檔案列表, 無效檔案列表)
    """
    valid_files = []
    invalid_files = []
    
    for file_path in file_paths:
        if is_supported_file(file_path):
            valid_files.append(file_path)
        else:
            invalid_files.append(file_path)
    
    return valid_files, invalid_files


def get_file_type(file_path: str) -> str:
    """
    取得檔案類型描述
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        str: 檔案類型 ('Image' 或 'PDF' 或 'Unknown')
    """
    if is_image_file(file_path):
        return "Image"
    elif is_pdf_file(file_path):
        return "PDF"
    else:
        return "Unknown"
