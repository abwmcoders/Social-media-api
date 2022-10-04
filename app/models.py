from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String,nullable=False, primary_key=False)
    content = Column(String,nullable=False, primary_key=False)
    published = Column(Boolean, primary_key=False, nullable=False, server_default='True',)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Votes(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

