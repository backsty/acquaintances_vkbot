import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"

    id = sq.Column(sq.INTEGER, primary_key=True)
    name = sq.Column(sq.VARCHAR(128), nullable=False)
    surname = sq.Column(sq.VARCHAR(128))
    sex = sq.Column(sq.VARCHAR(128))
    age = sq.Column(sq.INTEGER)
    city = sq.Column(sq.VARCHAR(256))
    vk_profile_id = sq.Column(sq.INTEGER, nullable=False)
    photos = relationship("Photos", back_populates="user")
    blocked_status = relationship("Blocklist", uselist=False, back_populates="user")
    favourites = relationship("Favourites", back_populates="user")
    likes = relationship("Likes", back_populates="user")

    def __str__(self):
        return f"Users {self.id}: {self.name} {self.surname} {self.vk_profile_id}"


class Blocklist(Base):
    __tablename__ = "Blocklist"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    user = relationship("Users", back_populates="blocked_status")
    is_blocked = sq.Column(sq.Boolean)

    def __str__(self):
        return f"User {self.user_id} Status: Blocked - {self.is_blocked}"


class Photos(Base):
    __tablename__ = "Photos"

    id = sq.Column(sq.INTEGER, primary_key=True)
    user_id = sq.Column(sq.INTEGER, sq.ForeignKey("Users.id"), nullable=False)
    user = relationship("Users", back_populates="photos")
    photo_url = sq.Column(sq.String(256))
    upload_date = sq.Column(sq.TIMESTAMP, server_default=sq.func.now())

    def __str__(self):
        return f"Users {self.id}: {self.user_id} {self.photo_url}"


class Likes(Base):
    __tablename__ = "Likes"

    id = sq.Column(sq.INTEGER, primary_key=True)
    photo_id = sq.Column(sq.INTEGER, sq.ForeignKey("Photos.id"), nullable=False)
    status_like = sq.Column(sq.BOOLEAN)
    user_id = sq.Column(sq.INTEGER, sq.ForeignKey("Users.id"))
    user = relationship("Users", back_populates="likes")

    def __str__(self):
        return f"Users {self.user_id}: {self.photo_id} {self.id} {self.status_like}"


class Favourites(Base):
    __tablename__ = "Favourites"

    id = sq.Column(sq.INTEGER, primary_key=True)
    user_id = sq.Column(sq.INTEGER, sq.ForeignKey("Users.id"), nullable=False)
    user = relationship("Users", back_populates="favourites")
    photo_id = sq.Column(sq.VARCHAR(128), sq.ForeignKey("Photos.id"), nullable=False)

    def __str__(self):
        return f"Users {self.id}: {self.user_id} {self.photo_id}"


class Matches(Base):
    __tablename__ = "Matches"

    id = sq.Column(sq.INTEGER, primary_key=True)
    user_id_receiver = sq.Column(sq.INTEGER, sq.ForeignKey("Users.id"))
    user_id_sender = sq.Column(sq.INTEGER, sq.ForeignKey("Users.id"))

    def __str__(self):
        return f"Users {self.id}: {self.user_id_receiver} - {self.user_id_sender}"


class Search_Weights(Base):
    __tablename__ = "Search_Weights"

    id = sq.Column(sq.INTEGER, primary_key=True)
    user_id = sq.Column(sq.INTEGER, sq.ForeignKey("Users.id"))
    age_weight = sq.Column(sq.INTEGER)
    gender_weight = sq.Column(sq.VARCHAR(128))
    common_groups = sq.Column(sq.VARCHAR(256))
    common_friends = sq.Column(sq.VARCHAR(256))
    music_interest_weight = sq.Column(sq.VARCHAR(1000))
    book_interest_weight = sq.Column(sq.VARCHAR(1000))

    def __str__(self):
        return f"Users {self.id}: {self.user_id}"


def create_tables(engine):
    """
    This function creates all tables defined in the SQLAlchemy Base metadata.

    The function uses the `create_all` method of the SQLAlchemy Base metadata object,
    which creates all tables stored in the metadata. All table definitions are usually done
    via the declarative base class and are accessible through the Base.metadata.tables dictionary.

    The `create_all` method checks the database for the existence of each table, and if it doesn't exist,
    the method creates it. Tables are created in the order of their foreign key dependencies.


    :param engine: engine (sqlalchemy.engine.Engine): The engine instance which is used to interface with the database.
    :return: None
    """
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)