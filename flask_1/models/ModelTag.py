from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import ModelBase, post_tags

class ModelTag(ModelBase):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True, nullable=False)

    # Posts
    posts = relationship('ModelPost', secondary=post_tags, back_populates='tags')

    def __repr__(self):
        return f'{self.tag_name}'