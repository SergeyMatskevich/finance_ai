from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.models import User, Family, Transaction, Budget, Account, UserRole
from app.core.security import get_password_hash
import os

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/family_finance")

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def init_db():
    try:
        # Проверяем, есть ли уже пользователи в базе
        if db.query(User).first() is None:
            # Создаем тестового пользователя
            test_user = User(
                email="test@example.com",
                hashed_password=get_password_hash("testpassword"),
                full_name="Test User",
                role=UserRole.ADMIN
            )
            db.add(test_user)
            db.commit()
            print("Test user created successfully")
        else:
            print("Database already initialized")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 