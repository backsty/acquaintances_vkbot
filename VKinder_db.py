from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    vk_id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    city = Column(Integer, nullable=False)
    step = Column(Integer, nullable=False)
    f_step = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("vk_id", name="unique_vk_id"),)

    def __str__(self):
        return f'{self.vk_id}:{self.vk_id}'


class SearchParameters(Base):
    __tablename__ = 'search_params'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.vk_id'))
    sex = Column(String)
    city = Column(Integer)
    age_from = Column(Integer)
    age_to = Column(Integer)
    user = relationship("User", backref="search_params")


class Matches(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    vk_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.vk_id'))
    step = Column(Integer, nullable=False)

    user = relationship("User", backref="matches")

    def __str__(self):
        return f'{self.name}:{self.surname}:{self.link}'


class Blacklisted(Base):
    __tablename__ = 'blacklisted'
    vk_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.vk_id"))
    user = relationship("User", backref="blacklisted")
    __table_args__ = (UniqueConstraint("vk_id", name="unique_blacklist_vk_id"),)


class Favorite(Base):
    __tablename__ = 'favorite'
    vk_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.vk_id"))
    f_step = Column(Integer, nullable=False)
    user = relationship("User", backref="favorite")


def create_bd(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
