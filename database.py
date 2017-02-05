from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy import create_engine

Base = declarative_base()


class Subscribe(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=False)


class User(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    caption = Column(String(250))
    genre = Column(String(8))


class Uploads(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('menu_item.id'))
    filename = Column(String(50))
    timestamp = Column(DateTime)


engine = create_engine('sqlite:///lantern.db')
Base.metadata.create_all(engine)