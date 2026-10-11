from sqlalchemy import Column, Integer, String,Text
from db import Base
from pydantic import BaseModel


# ========== 数据模型 ==========
class PageStat(Base):
    """页面访问统计表"""
    __tablename__ = "page_stats"

    page_path = Column(String, primary_key=True)
    total = Column(Integer, default=0)
    today = Column(Integer, default=0)
    last_date = Column(String)
    last_visit = Column(String)
    last_ip = Column(String)


class SiteStat(Base):
    """全局统计表（只有一行，id=1）"""
    __tablename__ = "site_stats"

    id = Column(Integer, primary_key=True, default=1)
    total = Column(Integer, default=0)
    today = Column(Integer, default=0)
    last_date = Column(String)