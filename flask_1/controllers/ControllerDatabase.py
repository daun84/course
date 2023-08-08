from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func, and_
from sqlalchemy.orm import relationship

from database import Session

from models.ModelPost import ModelPost
from models.ModelUser import ModelUser
from models.enums.EnumPostStatus import EnumPostStatus

from loguru import logger

from typing import List, Union

from flask import g

class ControllerDatabase:

    @staticmethod
    def get_user(
        username: str = None,
        email: str = None
        ) -> ModelUser:
        user = None
        try:
            assert (username is not None) ^ (email is not None), \
                "get_user function should take one parameter"
            filters = []
            if username:
                filters.append(ModelUser.user_name == username)
            if email:
                filters.append(ModelUser.user_email == email)

            user = g.db_session.query(ModelUser).filter(and_(*filters)).limit(1).first()

        except Exception as e:
            logger.error(e)

        return user


    @staticmethod
    def get_posts(
        post_author_id: int = None,
        post_id: int = None,
        url_slug: str = None,
        search_query: str = None,
        post_parent_id: int = None,
        status: EnumPostStatus = EnumPostStatus.published,
        get_one: bool = False
        ) -> Union[ModelPost, List[ModelPost]]: # is union a good practice?
        posts = None
        try:
            assert not (get_one and post_id is None and url_slug is None and search_query is None), \
                "get_posts function with get_one flag should have at least one identifier argument"
            filters = []
            if post_author_id is not None:
                filters.append(ModelPost.post_author_id == post_author_id)
            if post_id is not None:
                filters.append(ModelPost.post_id == post_id)
            if url_slug is not None:
                filters.append(ModelPost.post_url_slug == url_slug)
            if search_query is not None:
                filters.append(ModelPost.post_title.like(f'%{search_query}%'))
            if post_parent_id is not None:
                filters.append(ModelPost.post_parent_id == post_parent_id)

            filters.append(ModelPost.post_status == status)

            if get_one:
                posts = g.db_session.query(ModelPost).filter(and_(*filters)).limit(1).first()
            else:
                posts = g.db_session.query(ModelPost).filter(and_(*filters)).all()
            
        except Exception as e:
            logger.error(e)

        return posts
        
    @staticmethod
    def insert_user(user: ModelUser):
        try:
            g.db_session.add(user)
        except Exception as e:
            logger.error(e)

        
    @staticmethod
    def insert_post(post: ModelPost):
        try:
            g.db_session.add(post)
        except Exception as e:
            logger.error(e)    
    
    @staticmethod
    def delete_post(post: ModelPost):
        try:
            post.post_status = EnumPostStatus.deleted
            for child in post.child_posts:
                ControllerDatabase.delete_post(child)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def update_post(post: ModelPost):
        try:
            prefix_url = ""
            if post.parent_post:
                prefix_url = post.parent_post.post_url_slug + '/'

            parts = post.post_url_slug.rsplit('/', 1)
            post.post_url_slug = prefix_url + parts[-1]

            for child in post.child_posts:
                ControllerDatabase.update_post(child)

        except Exception as e:
            logger.error(e)
        