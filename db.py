from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite+pysqlite:///./test.db")	
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
from user.models import User

def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close()