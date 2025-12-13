import logging
import os
from typing import List, Dict, Any
import aiohttp
import asyncio

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("LLM_MODEL", "llama3.1:8b")
        self.timeout = 60

    async def generate_answer(self, question: str, context: List[Dict[str, Any]]) -> str:
        """Генерация ответа на основе контекста"""
        try:
            context_text = "\n\n".join([
                f"Источник: {doc.get('source', 'Неизвестно')}\nСодержание: {doc['content']}"
                for doc in context
            ])

            prompt = f"""Ты - ассистент по проектному обучению в университете. Ответь на вопрос студента, используя ТОЛЬКО предоставленную информацию из базы знаний.
            БАЗА ЗНАНИЙ:
            {context_text}
            
            ВОПРОС СТУДЕНТА: {question}
            
            ИНСТРУКЦИИ:
            1. ОТВЕЧАЙ ТОЛЬКО на основе информации из базы знаний выше
            2. Если информации для ответа недостаточно, честно скажи об этом
            3. Будь конкретным и полезным
            4. Форматируй ответ для лучшей читаемости
            
            ОТВЕТ:"""

            return await self._call_ollama(prompt)

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "Извините, произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте позже."

    async def _call_ollama(self, prompt: str) -> str:
        """Вызов локальной модели через Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/api/generate",
                        json={
                            "model": self.model,
                            "prompt": prompt,
                            "stream": False,
                            "options": {
                                "temperature": 0.3,
                                "top_p": 0.9,
                                "num_predict": 500
                            }
                        },
                        timeout=self.timeout
                ) as response:

                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get('response', '').strip()

                        if not response_text:
                            return "Не удалось получить ответ от модели."

                        return response_text
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama API error: {response.status} - {error_text}")
                        return f"Ошибка API: {response.status}"

        except aiohttp.ClientError as e:
            logger.error(f"Connection error to Ollama: {e}")
            return "Ошибка подключения к модели. Убедитесь, что Ollama запущен."
        except asyncio.TimeoutError:
            logger.error("Ollama API timeout")
            return "Превышено время ожидания ответа от модели."
        except Exception as e:
            logger.error(f"Unexpected error in Ollama call: {e}")
            return "Неожиданная ошибка при обращении к модели."