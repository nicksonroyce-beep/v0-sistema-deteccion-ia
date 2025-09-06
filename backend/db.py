from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, 
    **SQLALCHEMY_ENGINE_OPTIONS
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"Error de conexión a BD: {e}")
        return False
