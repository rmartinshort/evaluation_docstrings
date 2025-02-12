from abc import ABC, abstractmethod
from pdf2image import convert_from_bytes
import numpy as np
from PyPDF2 import PdfReader
import io
from receiptchat.data_transformations.constants import DEFAULT_DPI


class FileBytesToImage(ABC):
    @staticmethod
    @abstractmethod
    def convert_bytes_to_jpeg(file_bytes):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def convert_bytes_to_text(file_bytes):
        raise NotImplementedError


class PDFBytesToImage(FileBytesToImage):
    @staticmethod
    def convert_bytes_to_jpeg(file_bytes, dpi=DEFAULT_DPI, return_array=False):
        jpeg_data = convert_from_bytes(file_bytes, fmt="jpeg", dpi=dpi)[0]
        if return_array:
            jpeg_data = np.asarray(jpeg_data)
        return jpeg_data

    @staticmethod
    def convert_bytes_to_text(file_bytes):
        pdf_data = PdfReader(
            stream=io.BytesIO(initial_bytes=file_bytes)  # Create steam object
        )
        page = pdf_data.pages[0]
        return page.extract_text()
