from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite+pysqlite:///./test.db",connect_args={"check_same_thread": False},  # SQLite 多线程必须
    echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():  
    db = SessionLocal()
    try:  
        yield db  
    finally:  
        db.close()