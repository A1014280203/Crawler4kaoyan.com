from sqlalchemy import Column, Integer, Text, VARCHAR, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class KybSrc(Base):
    # 表的名字:
    __tablename__ = 'kybsrc'
    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    content = Column(Text)
    cls = Column(String(10))