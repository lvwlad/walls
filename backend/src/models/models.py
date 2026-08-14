from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

class Base(DeclarativeBase): pass

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    content: Mapped[list[dict]] = mapped_column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    owner = Column(Integer, ForeignKey('users.id'))

    users = relationship('User', uselist=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String)
    email = Column(String, unique=True)
    salt = Column(String)
    hash_password = Column(String)
    created_at = Column(Date)

    posts = relationship('Post')
    profile = relationship('Profile', uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bio = Column(String, default='') # it is a user desciption like I am a developer and a like to watch anime and .... 
    quote = Column(String, default='') # it is a quote like Stay hungry Stay foolish
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    banner = Column(String, default='') # it is a Minio image link 
    avatar = Column(String, default='') # it is a Minio image link 
    theme_color = Column(String, default='8B85C1') # keep string at HEX format

    users = relationship('User', uselist=False)




