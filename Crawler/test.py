from sqlalchemy import Column, String, create_engine, Integer, Text, VARCHAR, CHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义表对象:
class KybSrc(Base):
    # 表的名字:
    __tablename__ = 'kybsrc'
    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50))
    content = Column(Text)
    cls = Column(VARCHAR(10))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:password@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
new_info = KybSrc(title='t', content='c', cls='c')
session.add(new_info)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()