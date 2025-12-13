import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.knowledge_processor import KnowledgeProcessor
from services.vector_store import VectorStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def setup_knowledge_base():
    """Полная настройка базы знаний"""
    logger.info("Starting initial knowledge base setup...")

    vector_store = VectorStore()
    await vector_store.initialize()

    processor = KnowledgeProcessor()
    documents = processor.process_knowledge_base()

    logger.info(f"Processed {len(documents)} document chunks")

    if documents:
        await vector_store.add_documents(documents)
        logger.info("Knowledge base indexing completed successfully!")

        test_results = await vector_store.search("scrum", top_k=2)
        logger.info(f"Test search returned {len(test_results)} results")
    else:
        logger.error("No documents were processed!")


if __name__ == "__main__":
    asyncio.run(setup_knowledge_base())