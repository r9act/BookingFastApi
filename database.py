import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# Загружаем переменные из .env
load_dotenv()

# Читаем переменные окружения с значениями по умолчанию
DB_DRIVER = os.getenv("DB_DRIVER", "postgresql")
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Clubdata")

# Создаем URL для подключения
url = URL.create(
    drivername=DB_DRIVER,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# Создание движка и сессии
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Определение базового класса для моделей - лучше хранить в файле models.py
# Base = declarative_base()