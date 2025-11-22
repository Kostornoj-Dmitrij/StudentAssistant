import aiohttp
import logging
import os

logger = logging.getLogger(__name__)
RAG_API_URL = os.getenv('RAG_API_URL', 'http://localhost:8000')

class RAGClient:
    @staticmethod
    async def get_answer(question: str, user_id: int) -> str:
        """Реальный запрос к RAG API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{RAG_API_URL}/ask",
                        json={"question": question, "user_id": user_id},
                        timeout=30
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        answer = data.get('answer', 'Не удалось получить ответ')
                        sources = data.get('sources', [])

                        if sources:
                            answer += f"\n\n📚 Источники: {', '.join(sources)}"

                        return answer
                    else:
                        logger.error(f"RAG API error: {response.status}")
                        return "Извините, сервис временно недоступен. Попробуйте позже."

        except aiohttp.ClientError as e:
            logger.error(f"Connection error to RAG API: {e}")
            return "Ошибка подключения к сервису. Проверьте, запущен ли RAG API."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "Произошла непредвиденная ошибка."

    @staticmethod
    async def test_connection() -> bool:
        """Проверка подключения к RAG API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{RAG_API_URL}/health", timeout=5) as response:
                    return response.status == 200
        except:
            return False