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

    # Post author
    post_author_id = Column(Integer, ForeignKey('users.user_id'))
    post_author = relationship('ModelUser', back_populates="user_posts")

    # Children posts / Parent post
    post_parent_id = Column(Integer, ForeignKey('posts.post_id'), default=0)
    parent_post = relationship('ModelPost', remote_side=[post_id], back_populates='child_posts')
    child_posts = relationship('ModelPost', remote_side=[post_parent_id], back_populates='parent_post')

    def __repr__(self):
        return f'{self.post_title}, {self.post_url_slug}, {self.post_parent_id}, {self.post_status}'
