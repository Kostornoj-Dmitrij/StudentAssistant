from config import RAG_API_URL


class RAGClient:
    @staticmethod
    async def get_answer(question: str, user_id: int) -> str:
        """
        Заглушка для RAG-системы
        """
        demo_answers = {
            "scrum": """Скоро здесь будут точные ответы из базы знаний"""
        }

        question_lower = question.lower()

        if 'scrum' in question_lower:
            return demo_answers['scrum']
        elif 'agile' in question_lower:
            return demo_answers['agile']
        else:
            return demo_answers['default']

    @staticmethod
    async def test_connection() -> bool:
        try:
            return True
        except:
            return False