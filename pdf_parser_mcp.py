### Min
### PDF Parser MCP Tool
### Provides PDF parsing and chunking functionality for MCP server

from typing import Dict, Any, List
import PyPDF2
import pdfplumber
import re
from pathlib import Path

class PDFParserTool:
    name: str = "pdf_parser"

    inputSchema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "pdf_path": {"type": "string", "description": "PDF file path"},
            "parser_type": {"type": "string", "enum": ["default", "advanced"], "default": "advanced", "description": "Parser type"},
            "chunk_size": {"type": "integer", "default": 3, "description": "Number of sentences per chunk"}
        },
        "required": ["pdf_path"]
    }

    functions: List[str] = ["parse_pdf", "parse_folder"]

    def __init__(self):
        self.default_parser = PDFParser()
        self.advanced_parser = AdvancedPDFParser()

    def parse_pdf(self, pdf_path: str, parser_type: str = "advanced", chunk_size: int = 3) -> Dict[str, Any]:
        ### Parse a single PDF file and split into chunks
        try:
            if parser_type == "advanced":
                parser = self.advanced_parser
            else:
                parser = self.default_parser

            text = parser.extract_text_from_pdf(pdf_path)
            if not text.strip():
                return {"error": "No text extracted from PDF"}

            chunks = self._split_into_chunks(text, chunk_size)
            pdf_file = Path(pdf_path)

            return {
                "success": True,
                "file_name": pdf_file.name,
                "total_chunks": len(chunks),
                "chunks": chunks,
                "metadata": {
                    "file_size": pdf_file.stat().st_size,
                    "parser_type": parser_type,
                    "chunk_size": chunk_size
                }
            }
        except Exception as e:
            return {"error": f"Failed to parse PDF: {str(e)}"}

    def parse_folder(self, folder_path: str, parser_type: str = "advanced", chunk_size: int = 3) -> Dict[str, Any]:
        ### Parse all PDF files in a folder
        try:
            folder = Path(folder_path)
            if not folder.exists() or not folder.is_dir():
                return {"error": "Invalid folder path"}

            pdf_files = list(folder.glob("*.pdf"))
            if not pdf_files:
                return {"error": "No PDF files found in folder"}

            all_results = []
            total_chunks = 0

            for pdf_file in pdf_files:
                result = self.parse_pdf(str(pdf_file), parser_type, chunk_size)
                if result.get("success"):
                    all_results.append(result)
                    total_chunks += result["total_chunks"]

            return {
                "success": True,
                "total_files": len(all_results),
                "total_chunks": total_chunks,
                "files": all_results
            }
        except Exception as e:
            return {"error": f"Failed to parse folder: {str(e)}"}

    def _split_into_chunks(self, text: str, chunk_size: int) -> List[str]:
        ### Split text into chunks by sentence
        sentences = re.split(r'(?<=[.?!])\\s+', text.strip())
        chunks = []
        temp = []

        for sentence in sentences:
            temp.append(sentence)
            if len(temp) >= chunk_size:
                chunks.append(" ".join(temp))
                temp = []

        if temp:
            chunks.append(" ".join(temp))

        return chunks

class PDFParser:
    def extract_text_from_pdf(self, pdf_path):
        ### Extract text using PyPDF2
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\\n"
            return text

class AdvancedPDFParser:
    def extract_text_from_pdf(self, pdf_path):
        ### Extract text using pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\\n"
        return text
### #%#