import aiosqlite
import asyncio

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file

    async def initialize(self):
        """Создание таблиц, если они не существуют."""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                telegram_id TEXT,
                object_id TEXT,
                photos TEXT,
                additional_photos TEXT,
                workDoneWith TEXT,
                wishList TEXT,
                toRepair TEXT,
                startTime TEXT,
                finishTime TEXT,
                finished BOOLEAN DEFAULT 0
            )
        """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT NOT NULL,
                    telegram_id TEXT NOT NULL UNIQUE
                )
            """)
            
            await db.commit()
            print("Таблицы 'tasks' и 'users' созданы.")

    async def add_task(
        self,
        phone_number: str,
        telegram_id: str,
        object_id: str,
        photos: str,
        additional_photos: str,
        work_done_with: str,
        wish_list: str,
        to_repair: str,
        start_time: str,
        finish_time: str,
        finished: bool = False
        ):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                INSERT INTO tasks (
                    phone_number,
                    telegram_id,
                    object_id,
                    photos,
                    additional_photos,
                    workDoneWith,
                    wishList,
                    toRepair,
                    startTime,
                    finishTime,
                    finished
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                phone_number,
                telegram_id,
                object_id,
                photos,
                additional_photos,
                work_done_with,
                wish_list,
                to_repair,
                start_time,
                finish_time,
                finished
            ))
            await db.commit()


    async def add_user(self, phone_number, telegram_id):
        """Добавление пользователя в таблицу users."""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                INSERT OR IGNORE INTO users (phone_number, telegram_id)
                VALUES (?, ?)
            """, (phone_number, telegram_id))
            await db.commit()



    async def get_user_by_telegram_id(self, telegram_id):
        async with aiosqlite.connect(self.db_file) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            user = await cursor.fetchone()
            return user


    async def get_all_tasks(self):
        """Получение всех записей из таблицы tasks."""
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT * FROM tasks")
            rows = await cursor.fetchall()
            return rows

    async def get_tasks_by_phone(self, phone_number):
        """Поиск задач по номеру телефона."""
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT * FROM tasks WHERE phone_number = ?", (phone_number,))
            rows = await cursor.fetchall()
            return rows