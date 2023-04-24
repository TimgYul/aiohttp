from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, BOOLEAN
import uuid

engine = create_engine('postgresql://postgres:12121987@127.0.0.1:5432/flask_db')
# engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5431/flask_db')
Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    is_admin = Column(BOOLEAN, nullable=False, default=False)
    
class UserPost(Base):
    __tablename__ = 'user_posts'
    
    id = Column(Integer, autoincrement=True, primary_key=True )
    creator = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_header = Column(String, nullable=False)
    post_text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
Base.metadata.create_all()