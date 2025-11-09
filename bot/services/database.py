import os
from contextlib import asynccontextmanager

from aiosqlite import connect, Row


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
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    question TEXT,
                    answer TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')

            await conn.commit()

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
                "INSERT INTO users (username, user_id) VALUES (?, ?)",
                (username, user_id)
            )
            await conn.commit()

    async def add_question(self, user_id: int, question: str, answer: str):
        async with self.get_connection() as conn:
            await conn.execute(
                '''INSERT INTO questions (user_id, question, answer)
                   VALUES (?, ?, ?)''',
                (user_id, question, answer)
            )
            await conn.commit()

    async def get_user_questions(self, user_id: int, limit: int = 10):
        async with self.get_connection() as conn:
            cursor = await conn.execute(
                '''SELECT question, answer, created_at 
                   FROM questions 
                   WHERE user_id = ? 
                   ORDER BY created_at DESC 
                   LIMIT ?''',
                (user_id, limit)
            )
            return await cursor.fetchall()


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_file = os.path.join(project_dir, 'data', 'project_assistant.db')

os.makedirs(os.path.dirname(db_file), exist_ok=True)

db = Database(db_file)