from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import ModelBase

class ModelUser(ModelBase):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, unique=True, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String, nullable=False)

    # Posts
    user_posts = relationship('ModelPost', back_populates='post_author')

    def __repr__(self):
        return f'{self.user_name}'