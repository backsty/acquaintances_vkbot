import sqlalchemy as sq
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    city = Column(String)
    gender = Column(String)
    vk_profile = Column(String)
    photos = relationship("Photo", backref="user")
    blacklist = relationship("Blacklist", backref="user")
    favorites = relationship("Favorites", backref="user")
    interests = relationship("UserInterests", backref="user")


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    likes = Column(Integer)


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))


class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))


class UserInterests(Base):
    __tablename__ = 'user_interests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    interest = Column(String)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres:admin@localhost:5432/vkbot_2"
engine = sq.create_engine(DSN)
create_tables(engine)
