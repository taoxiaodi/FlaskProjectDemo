from work.orm import mode
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
session = sessionmaker()()
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/memberdb",
                       encoding='utf8', echo=True)


def insert(username, password):
        session.add(mode.User(username=username, password=password))
        session.commit()
        # session.close()


def find(username, password):
    user = session.query(mode.User).filter(mode.User.username == username).filter(mode.User.password == password).first()
    result = str(user.id) + '|' + user.username
    if result:
        return result
    else:
        return -1


def add_project(name, details, user_id):
    session.add(mode.Project(name=name, details=details, user_id=user_id))
    session.commit()
    session.close()


def read_project(user_id):
    user = session.query(mode.Project).filter(mode.Project.user_id == user_id).all()
    return user


def amend(user_id, name, details):
    session.query(mode.Project).filter(mode.Project.id == user_id).update({
        mode.Project.name: name, mode.Project.details: details})
    session.commit()


def read_pro(ids):
    user = session.query(mode.Project).filter(mode.Project.id == ids).first()
    return user


def del_user(user_id):
    session.query(mode.Project).filter(mode.Project.id == user_id).delete()
    session.commit()

read_pro(1)