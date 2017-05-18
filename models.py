from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Category(Base):
    """The categories of the measurements"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=None)
    is_integer = Column(Boolean, nullable=None)


class Measurement(Base):
    """The measurements"""
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=None)
    timestamp = Column(DateTime, nullable=None)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', backref='measurements')


def create_database_session(database_uri):
    """Create a new database session."""
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    return session
