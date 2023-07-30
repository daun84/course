from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship

from database import ModelBase

from models.enums.EnumPostStatus import EnumPostStatus

class ModelPost(ModelBase):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    post_url_slug = Column(String, default="")
    post_title = Column(String, nullable=False)
    post_body = Column(String, nullable=False)
    post_thumbnail_uuid = Column(String)
    post_created = Column(DateTime)
    post_modified = Column(DateTime)
    post_status = Column(Enum(EnumPostStatus), default=EnumPostStatus.not_set)

    #relationships
    post_author_id = Column(Integer, ForeignKey('users.user_id'))
    post_author = relationship('ModelUser', back_populates="user_posts")

    def __repr__(self):
        return f'{self.post_title}, {self.post_url_slug}, {self.post_author_id}, {self.post_status}'
