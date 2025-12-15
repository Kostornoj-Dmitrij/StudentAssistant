import os
import PyPDF2
import docx
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class KnowledgeProcessor:
    def __init__(self, knowledge_base_path: str = "/app/knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        logger.info(f"Initialized KnowledgeProcessor with path: {knowledge_base_path}")

    def process_knowledge_base(self) -> List[Dict[str, str]]:
        """Обработка всей базы знаний и создание чанков"""
        logger.info(f"Starting processing of knowledge base at: {self.knowledge_base_path}")
        documents = []

        for root, dirs, files in os.walk(self.knowledge_base_path):
            for file in files:
                file_path = os.path.join(root, file)
                logger.debug(f"Processing file: {file_path}")
                file_docs = self._process_file(file_path)
                documents.extend(file_docs)

        logger.info(f"Processing complete")
        logger.info(f"Processed {len(documents)} document chunks")
        return documents

    def _process_file(self, file_path: str) -> List[Dict[str, str]]:
        """Обработка отдельного файла"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()

            if file_ext == '.pdf':
                return self._process_pdf(file_path)
            elif file_ext == '.docx':
                return self._process_docx(file_path)
            elif file_ext in ['.txt', '.md']:
                return self._process_text(file_path)
            else:
                logger.warning(f"Unsupported file format: {file_path}")
                return []

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []

    def _process_pdf(self, file_path: str) -> List[Dict[str, str]]:
        """Обработка PDF файла"""
        documents = []
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        chunks = self._split_text(text, chunk_size=1000, overlap=50)

                        for i, chunk in enumerate(chunks):
                            documents.append({
                                'content': chunk,
                                'source': f"{os.path.basename(file_path)} - стр. {page_num + 1}",
                                'file_path': file_path
                            })

        except Exception as e:
            logger.error(f"PDF processing error {file_path}: {e}")

        return documents

    def _process_docx(self, file_path: str) -> List[Dict[str, str]]:
        """Обработка DOCX файла"""
        try:
            doc = docx.Document(file_path)
            full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

            chunks = self._split_text(full_text, chunk_size=1000, overlap=50)
            return [{
                'content': chunk,
                'source': os.path.basename(file_path),
                'file_path': file_path
            } for chunk in chunks]

        except Exception as e:
            logger.error(f"DOCX processing error {file_path}: {e}")
            return []

    def _process_text(self, file_path: str) -> List[Dict[str, str]]:
        """Обработка текстового файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            chunks = self._split_text(text, chunk_size=1000, overlap=50)
            return [{
                'content': chunk,
                'source': os.path.basename(file_path),
                'file_path': file_path
            } for chunk in chunks]

        except Exception as e:
            logger.error(f"Text processing error {file_path}: {e}")
            return []

    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Разбивка текста на чанки с перекрытием"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            if end < len(text):
                while end > start and text[end] not in ['.', '!', '?', '\n']:
                    end -= 1
                if end == start:
                    end = start + chunk_size

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - overlap

        return chunks