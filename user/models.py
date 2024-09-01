from sqlalchemy import Column, Integer, String,Text
from db import Base
from pydantic import BaseModel


# ORM
class User(Base):
    __tablename__ = 'users'		# 定义数据库中表名
    id = Column(Integer, primary_key=True)  
    username = Column(String(80), unique=True, nullable=False)  
    password_hash = Column(String(128), nullable=False) 

# 参数认证
class User_data(BaseModel):
    username: str
    password: str