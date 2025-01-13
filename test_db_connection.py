from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем параметры подключения из переменных окружения
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Формируем строку подключения
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем движок
engine = create_engine(DATABASE_URL)

# Создаем базовый класс для моделей
Base = declarative_base()

# Пример базовой модели
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def test_connection():
    try:
        # Пробуем создать таблицы
        Base.metadata.create_all(engine)
        
        # Создаем сессию
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Пробуем создать тестового пользователя
        test_user = User(
            username='test_user',
            email='test@example.com'
        )
        
        session.add(test_user)
        session.commit()
        
        # Проверяем, что пользователь создался
        queried_user = session.query(User).filter_by(username='test_user').first()
        print(f"Тестовый пользователь создан с id: {queried_user.id}")
        
        # Удаляем тестового пользователя
        session.delete(queried_user)
        session.commit()
        
        print("Подключение к БД успешно установлено и протестировано!")
        return True
        
    except Exception as e:
        print(f"Ошибка при подключении к БД: {str(e)}")
        return False
    
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    test_connection()