from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func, and_
from sqlalchemy.orm import relationship, joinedload

from database import Session, post_tags

from models.ModelPost import ModelPost
from models.ModelUser import ModelUser
from models.ModelTag import ModelTag
from models.enums.EnumPostStatus import EnumPostStatus

from loguru import logger

from typing import List, Union

from flask import g

from utils.get_single_or_list import get_single_or_list

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

            query = g.db_session.query(ModelUser)
            filtered_query = query.filter(and_(*filters)).limit(1)
            user = filtered_query.first()

        except Exception as e:
            logger.error(e)

        return user


    @staticmethod
    @get_single_or_list
    def get_posts(
        post_author_id: int = None,
        post_tag: ModelTag = None,
        post_id: int = None,
        url_slug: str = None,
        search_query: str = None,
        post_parent_id: int = None,
        status: EnumPostStatus = EnumPostStatus.published,
        get_one: bool = False
        ) -> List[ModelPost]:
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
            if post_tag is not None:
                filters.append(post_tags.c.tag_id == post_tag.tag_id)

            filters.append(ModelPost.post_status == status)

            limit = None
            if get_one:
                limit = 1

            query = g.db_session.query(ModelPost)
            filtered_query = query.filter(and_(*filters))
            optioned_query = filtered_query.options(joinedload(ModelPost.tags))
            limited_query = optioned_query.limit(limit)
            posts = limited_query.all()

            
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
            g.db_session.commit()
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

    @staticmethod
    @get_single_or_list
    def get_tags(
        tag_name: str = None,
        tag_id: int = None,
        get_one: bool = False
        ) -> List[ModelTag]:
        tags = []
        try:
            assert not (get_one and tag_id is None and tag_name is None), \
                "get_tags function with get_one flag should have at least one identifier argument"
            filters = []

            if tag_name is not None:
                filters.append(ModelTag.tag_name == tag_name)
            if tag_id is not None:
                filters.append(ModelTag.tag_id == tag_id)

            limit = None
            if get_one:
                limit = 1 

            query = g.db_session.query(ModelTag)
            filtered_query = query.filter(and_(*filters))
            limited_query = filtered_query.limit(limit)
            tags = limited_query.all()

            
        except Exception as e:
            logger.error(e)

        return tags

    
    @staticmethod
    def delete_tag(tag: ModelTag):
        try:
            g.db_session.delete(tag)
            g.db_session.commit()
        except Exception as e:
            logger.error(e)

    
    @staticmethod
    def insert_tag(tag: ModelTag):
        try:
            g.db_session.add(tag)
            g.db_session.commit()
        except Exception as e:
            logger.error(e)  