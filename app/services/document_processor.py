from typing import List, Dict
from pathlib import Path
import pypdf
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> str:
        """Load text from PDF"""
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def load_docx(self, file_path: str) -> str:
        """Load text from DOCX"""
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    def load_txt(self, file_path: str) -> str:
        """Load text from TXT"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def process_document(self, file_path: str) -> List[Dict]:
        """Process document and return chunks with metadata"""
        path = Path(file_path)
        
        # Load based on extension
        if path.suffix == '.pdf':
            text = self.load_pdf(file_path)
        elif path.suffix == '.docx':
            text = self.load_docx(file_path)
        elif path.suffix == '.txt':
            text = self.load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Split into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Add metadata
        chunk_data = []
        for idx, chunk in enumerate(chunks):
            chunk_data.append({
                "text": chunk,
                "metadata": {
                    "source": path.name,
                    "chunk_index": idx,
                    "total_chunks": len(chunks)
                }
            })
        
        return chunk_data
