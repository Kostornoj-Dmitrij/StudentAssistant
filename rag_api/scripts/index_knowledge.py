import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_api.services.knowledge_processor import KnowledgeProcessor
from rag_api.services.vector_store import VectorStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция индексации базы знаний"""
    logger.info("Starting knowledge base indexing...")

    processor = KnowledgeProcessor()
    documents = processor.process_knowledge_base()

    logger.info(f"Processed {len(documents)} document chunks")

    vector_store = VectorStore()
    await vector_store.initialize()
    await vector_store.add_documents(documents)

    logger.info("Knowledge base indexing completed!")


if __name__ == "__main__":
    asyncio.run(main())