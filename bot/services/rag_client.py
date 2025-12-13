import asyncio

import aiohttp
import logging
import os

logger = logging.getLogger(__name__)
RAG_API_URL = os.getenv('RAG_API_URL', 'http://localhost:8000')

class RAGClient:
    @staticmethod
    async def get_answer(question: str, user_id: int, max_retries: int = 3) -> str:
        """Запрос к RAG API"""
        last_error = None

        for attempt in range(max_retries):
            try:
                logger.info(f"Попытка {attempt + 1}/{max_retries} получения ответа для пользователя {user_id}")
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
                            last_error = f"HTTP ошибка: {response.status}"
                            logger.error(f"RAG API error: {response.status}")
                            if attempt < max_retries - 1:
                                await asyncio.sleep(2 ** attempt)
            except aiohttp.ClientError as e:
                last_error = f"Ошибка подключения: {e}"
                logger.error(f"Connection error to RAG API: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
            except Exception as e:
                last_error = f"Непредвиденная ошибка: {e}"
                logger.error(f"Unexpected error: {e}")
                break
        error_msg = f"❌ Не удалось получить ответ после {max_retries} попыток. Последняя ошибка: {last_error}"
        logger.error(error_msg)
        return "Извините, сервис временно недоступен. Попробуйте задать вопрос позже."

    @staticmethod
    async def test_connection() -> bool:
        """Проверка подключения к RAG API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{RAG_API_URL}/health", timeout=5) as response:
                    return response.status == 200
        except:
            return False