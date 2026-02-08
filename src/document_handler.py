"""Document parsing and handling utilities."""

import json
from pathlib import Path

import PyPDF2
from docx import Document


class DocumentHandler:
    """Handles document parsing and extraction."""

    SUPPORTED_FORMATS = {".pdf", ".docx", ".txt"}

    @staticmethod
    def extract_input_text(file_path: str) -> str:
        """
        Extract text from various document formats.

        Args:
            file_path: Path to the document file

        Returns:
            Extracted text content

        Raises:
            ValueError: If file format is not supported
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext not in DocumentHandler.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {DocumentHandler.SUPPORTED_FORMATS}"
            )

        if file_ext == ".pdf":
            return DocumentHandler._extract_from_pdf(file_path)
        elif file_ext == ".docx":
            return DocumentHandler._extract_from_docx(file_path)
        elif file_ext == ".txt":
            return DocumentHandler._extract_from_txt(file_path)

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text