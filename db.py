from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import model


def make_db_session():
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:password@localhost:3306/test?charset=utf8')
    # 创建DBSession类型:
    db_session = sessionmaker(bind=engine)
    # 实例化
    session = db_session()
    return session

if __name__ == '__main__':
    newm = model.KybSrc(title='啊啊', content='qwe123!@#qq', cls='ww')
    session = make_db_session()
    session.add(newm)
    session.commit()
    session.close()