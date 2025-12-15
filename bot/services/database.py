import logging
import os
from contextlib import asynccontextmanager

from aiosqlite import connect, Row

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db = not os.path.exists(db_path)

    @asynccontextmanager
    async def get_connection(self):
        db = await connect(self.db_path)
        db.row_factory = Row
        try:
            yield db
        finally:
            await db.close()

    async def init_database(self):
        """Инициализация базы данных"""
        async with self.get_connection() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS qa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    answer_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions (id),
                    FOREIGN KEY (answer_id) REFERENCES answers (id),
                    UNIQUE(question_id, answer_id)
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    comment TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions (id)
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    source_name TEXT NOT NULL,
                    source_page INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions (id)
                )
            ''')

            await conn.commit()
            logger.info("Все таблицы базы данных созданы")

    async def seed_test_data(self):
        """Заполнение тестовыми данными для демонстрации"""
        async with self.get_connection() as conn:
            cursor = await conn.execute("SELECT COUNT(*) as count FROM users")
            result = await cursor.fetchone()

            if result['count'] > 0:
                logger.info("Тестовые данные уже существуют, пропускаем заполнение")
                return

            test_users = [
                (123456789, "test_user_1"),
                (987654321, "test_user_2"),
                (555555555, "student_project"),
                (777777777, "team_lead_user"),
            ]

            for user_id, username in test_users:
                await conn.execute(
                    "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                    (user_id, username)
                )

            test_qa = [
                (123456789, "Как составить план проекта?",
                 "Для составления плана проекта необходимо:\n1. Определить цели и задачи\n2. Разбить проект на этапы\n3. Оценить ресурсы и сроки\n4. Назначить ответственных\n5. Создать расписание работ"),

                (987654321, "Что такое Scrum?",
                 "Scrum - это гибкая методология управления проектами, основанная на:\n• Спринтах (коротких итерациях)\n• Ежедневных стендапах\n• Бэклоге продукта\n• Ретроспективах"),

                (555555555, "Как провести эффективную встречу команды?",
                 "Для эффективной встречи:\n1. Подготовьте повестку заранее\n2. Определите временные рамки\n3. Назначьте модератора\n4. Делайте заметки\n5. Завершите с четкими action items"),

                (777777777, "Какие документы нужны для проекта?",
                 "Основные документы проекта:\n• Техническое задание\n• План проекта\n• Протоколы встреч\n• Отчеты о ходе работ\n• Финальный отчет"),
            ]

            for user_id, question, answer in test_qa:
                cursor = await conn.execute(
                    "INSERT INTO questions (user_id, question) VALUES (?, ?)",
                    (user_id, question)
                )
                question_id = cursor.lastrowid

                cursor = await conn.execute(
                    "INSERT INTO answers (user_id, answer) VALUES (?, ?)",
                    (user_id, answer)
                )
                answer_id = cursor.lastrowid

                await conn.execute(
                    "INSERT INTO qa (question_id, answer_id) VALUES (?, ?)",
                    (question_id, answer_id)
                )

            await conn.execute(
                "INSERT INTO feedback (question_id, rating, comment) VALUES (?, ?, ?)",
                (1, 5, "Отличный развернутый ответ!")
            )

            await conn.commit()
            logger.info("Тестовые данные успешно добавлены в базу")

    async def get_user(self, user_id: int):
        async with self.get_connection() as conn:
            cursor = await conn.execute(
                'SELECT * FROM users WHERE user_id = ?',
                (user_id,)
            )
            return await cursor.fetchone()

    async def create_user(self, username: str, user_id: int):
        async with self.get_connection() as conn:
            await conn.execute(
                "INSERT OR IGNORE INTO users (username, user_id) VALUES (?, ?)",
                (username, user_id)
            )
            await conn.commit()

    async def add_question_answer(self, user_id: int, question: str, answer: str):
        """Добавление вопроса и ответа в базу"""
        async with self.get_connection() as conn:
            try:
                user = await self.get_user(user_id)
                if not user:
                    username = f"user_{user_id}"
                    await self.create_user(username, user_id)

                cursor = await conn.execute(
                    "INSERT INTO questions (user_id, question) VALUES (?, ?)",
                    (user_id, question)
                )
                question_id = cursor.lastrowid

                cursor = await conn.execute(
                    "INSERT INTO answers (user_id, answer) VALUES (?, ?)",
                    (user_id, answer)
                )
                answer_id = cursor.lastrowid

                await conn.execute(
                    "INSERT INTO qa (question_id, answer_id) VALUES (?, ?)",
                    (question_id, answer_id)
                )

                await conn.commit()
                logger.info(f"Добавлен Q&A для пользователя {user_id}")

                return question_id, answer_id

            except Exception as e:
                logger.error(f"Ошибка при добавлении Q&A: {e}")
                await conn.rollback()
                raise

    async def get_user_stats(self, user_id: int):
        """Получение статистики пользователя"""
        async with self.get_connection() as conn:
            cursor = await conn.execute('''
                SELECT 
                    COUNT(DISTINCT q.id) as total_questions,
                    COUNT(DISTINCT a.id) as total_answers,
                    MIN(q.created_at) as first_question_date
                FROM users u
                LEFT JOIN questions q ON u.user_id = q.user_id
                LEFT JOIN answers a ON u.user_id = a.user_id
                WHERE u.user_id = ?
                GROUP BY u.id
            ''', (user_id,))

            return await cursor.fetchone()

    async def get_recent_questions(self, user_id: int, limit: int = 5):
        """Получение последних вопросов пользователя"""
        async with self.get_connection() as conn:
            cursor = await conn.execute('''
                SELECT 
                    q.question,
                    a.answer,
                    q.created_at
                FROM questions q
                JOIN qa ON q.id = qa.question_id
                JOIN answers a ON qa.answer_id = a.id
                WHERE q.user_id = ?
                ORDER BY q.created_at DESC
                LIMIT ?
            ''', (user_id, limit))

            return await cursor.fetchall()


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_file = os.path.join(project_dir, 'data', 'project_assistant.db')

os.makedirs(os.path.dirname(db_file), exist_ok=True)

db = Database(db_file)