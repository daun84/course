import flask
from flask import request, redirect, url_for, render_template, flash, session, g

from models.ModelUser import ModelUser
from models.ModelPost import ModelPost
from models.enums.EnumPostStatus import EnumPostStatus

from controllers.ControllerDatabase import ControllerDatabase

from sqlalchemy import and_, func

from utils.login_required import login_reqired

from loguru import logger


class ControllerPosts:
    blueprint = flask.Blueprint("posts", __name__, url_prefix="/posts")

    @staticmethod
    @blueprint.route('/')
    def published_posts():
        result = None

        try:
            success_message = request.args.get('success_message')
            query = request.args.get('query', default=None)

            if query is None:
                all_posts = ControllerDatabase.get_posts(post_parent_id=0)
                result = render_template('home.html', posts=all_posts, success_message=success_message)
            else:
                query_posts = ControllerDatabase.get_posts(search_query=query, post_parent_id=0)
                result = render_template('home.html', posts=query_posts, search=True, success_message=success_message)
        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")

        return result

    @staticmethod
    @blueprint.route('/new', methods=["POST", "GET"])
    @blueprint.route('/edit/<path:url_slug>', methods=["POST", "GET"])
    @login_reqired
    def edit(url_slug=None):
        result = None

        try:
            post = None
            is_editing = url_slug is not None
            parent_id = (int)(request.args.get('parent_id', 0))

            if is_editing:
                post = ControllerDatabase.get_posts(get_one=True, url_slug=url_slug)

            result = render_template('edit_post.html', post=post, is_editing=is_editing, parent_id=parent_id)

            if is_editing and post is None:
                result = redirect(url_for('posts.published_posts'))
            elif request.method == "POST":
                
                action = request.form.get('action')

                if 'submit' == action:
                    slug = request.form.get('url_slug').strip()
                    url_prefix: str = ""
            
                    if is_editing:
                        last_slash_index = url_slug.rfind('/')
                        url_prefix = url_slug[:last_slash_index + 1]
                    elif parent_id != 0:
                        parent_post = ControllerDatabase.get_posts(get_one=True, post_id=parent_id)
                        url_prefix = parent_post.post_url_slug + '/'

                    final_slug: str = url_prefix + slug 

                    existing_posts = ControllerDatabase.get_posts(url_slug=final_slug)

                    if ' ' in slug or '/' in slug:
                        error = "This url_slug is not allowed"
                        result = render_template('edit_post.html', post=post, error_message=error, is_editing=is_editing, parent_id=parent_id)
                    elif not (len(existing_posts) == 0 or \
                        len(existing_posts) == 1 and post in existing_posts):
                        error = "This url_slug is already being used"
                        result = render_template('edit_post.html', post=post, error_message=error, is_editing=is_editing, parent_id=parent_id)
                    else:
                        if not is_editing:
                            post = ModelPost()
                            post.post_status = EnumPostStatus.published
                            post.post_author = g.user
                            post.post_created = func.now()
                            post.post_parent_id = parent_id

                        post.post_title = request.form.get('title').strip()
                        post.post_body = request.form.get('body').strip()
                        post.post_url_slug = final_slug
                        post.post_modified = func.now()
                        ControllerDatabase.insert_post(post)

                        if is_editing:
                            ControllerDatabase.update_post(post)

                        success_message = "Post edited" if is_editing else "Post created" 

                        result = redirect(url_for('posts.published_posts', success_message=success_message))
                elif 'delete' == action:
                    ControllerDatabase.delete_post(post)
                    success_message = "Post deleted"
                    result = redirect(url_for('posts.published_posts', success_message=success_message))
        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")
            
        return result


    @staticmethod
    @blueprint.route('/view/<path:url_slug>')
    def view(url_slug):
        result = None

        try:
            post = ControllerDatabase.get_posts(get_one=True, url_slug=url_slug)

            if post is None:
                result = redirect(url_for('posts.published_posts'))
            else:
                sub_posts = ControllerDatabase.get_posts(post_parent_id=post.post_id)
                result = render_template('view.html', post=post, sub_posts=sub_posts)
        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")

        return result

    
