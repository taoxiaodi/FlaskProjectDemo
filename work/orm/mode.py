from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer,ForeignKey


engine = create_engine("mysql+mysqlconnector://root:123456@localhost/memberdb",
                       encoding='utf8', echo=True)

Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(20), nullable=False)
    details = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
