import chromadb
from chromadb.config import Settings
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self.client = None
        self.collection = None
        self.collection_name = "project_knowledge"

    async def initialize(self):
        """Инициализация векторной БД"""
        try:
            self.client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "База знаний по проектному обучению"}
            )

            logger.info(f"Vector store initialized. Collection: {self.collection_name}")

        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise

    async def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Поиск релевантных документов"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )

            documents = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'source': results['metadatas'][0][i].get('source', 'unknown') if results[
                            'metadatas'] else 'unknown',
                        'distance': results['distances'][0][i] if results['distances'] else 0
                    })

            return documents

        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    async def add_documents(self, documents: List[Dict[str, str]]):
        """Добавление документов в векторную БД"""
        try:
            texts = [doc['content'] for doc in documents]
            metadatas = [{'source': doc['source']} for doc in documents]
            ids = [f"doc_{i}" for i in range(len(documents))]

            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )

            logger.info(f"Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise