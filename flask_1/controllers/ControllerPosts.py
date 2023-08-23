import flask
from flask import request, redirect, url_for, render_template, flash, session, g

from models.ModelUser import ModelUser
from models.ModelPost import ModelPost
from models.ModelTag import ModelTag
from models.enums.EnumPostStatus import EnumPostStatus

from controllers.ControllerDatabase import ControllerDatabase

from sqlalchemy import and_, func

from utils.login_required import login_reqired

from loguru import logger

from database import post_tags

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
            tags = ControllerDatabase.get_tags()
            alredy_selected_tags = []

            if is_editing:
                post = ControllerDatabase.get_posts(get_one=True, url_slug=url_slug)
                alredy_selected_tags = post.tags

            result = render_template('edit_post.html', post=post, is_editing=is_editing, parent_id=parent_id, tags=tags, selected_tags=alredy_selected_tags)

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
                        result = render_template('edit_post.html', post=post, error_message=error, is_editing=is_editing, parent_id=parent_id, tags=tags)
                    elif not (len(existing_posts) == 0 or \
                        len(existing_posts) == 1 and post in existing_posts):
                        error = "This url_slug is already being used"
                        result = render_template('edit_post.html', post=post, error_message=error, is_editing=is_editing, parent_id=parent_id, tags=tags)
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

                        post.tags.clear()
                        g.db_session.commit()

                        selected_tags = request.form.getlist('tags')

                        for t_name in selected_tags:
                            new_tag = ControllerDatabase.get_tags(get_one=True, tag_name=t_name)
                            post.tags.append(new_tag)
                            g.db_session.commit()

                        if is_editing:
                            ControllerDatabase.update_post(post)

                        g.db_session.commit()

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


    @staticmethod
    @blueprint.route('/tags', methods=["POST", "GET"])
    @login_reqired 
    def tags():
        result = None

        try: 
            success_message = request.args.get('success_message')   
            tags = ControllerDatabase.get_tags()
            result = render_template('tags.html', tags=tags, success_message=success_message)

            if request.method == "POST":
                tag_name = request.form.get('tag_name').strip()
                tag = ControllerDatabase.get_tags(get_one=True, tag_name=tag_name)
                if tag:
                    error = "This tag is already being used"
                    result = render_template('tags.html', tags=tags, error_message=error)
                else:
                    tag = ModelTag()
                    tag.tag_name = tag_name
                    logger.info(tag)
                    ControllerDatabase.insert_tag(tag)
                    success_message = "New tag created"
                    tags.append(tag)
                    result = render_template('tags.html', tags=tags, success_message=success_message)
                    
        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")
        
        return result


    @staticmethod
    @blueprint.route('/edit_tag/<tag_name>', methods=["POST", "GET"])
    @login_reqired
    def edit_tag(tag_name=None):
        result = None

        try:
            tag = None
            sub_posts = None

            # Finding tag
            if tag_name is None:
                pass
            else:
                tag = ControllerDatabase.get_tags(get_one=True, tag_name=tag_name)
                if not tag:
                     tag = None
            
            if tag is None:
                result = redirect(url_for('posts.tags'))
            else:
                sub_posts = ControllerDatabase.get_posts(post_tag=tag)
                result = render_template('edit_tag.html', tag=tag, sub_posts=sub_posts)

            if request.method == "POST":
                action = request.form.get('action')

                if action == "submit":
                    new_tag_name = request.form.get('tag_name').strip()
                    eixsting_tag = ControllerDatabase.get_tags(get_one=True, tag_name=new_tag_name)
                    if eixsting_tag:
                        error = "This tag is already being used"
                        result = render_template('edit_tag.html', tag=tag, error_message=error, sub_posts=sub_posts)
                    else:
                        tag.tag_name = new_tag_name
                        g.db_session.commit()
                        success_message = "Tag updated"
                        result = redirect(url_for('posts.tags', success_message=success_message))
                elif action == "delete":
                    if sub_posts:
                        error = "This tag is being used"
                        result = render_template('edit_tag.html', tag=tag, error_message=error, sub_posts=sub_posts)
                    else:
                        ControllerDatabase.delete_tag(tag)
                        success_message = "Tag deleted"
                        result = redirect(url_for('posts.tags', success_message=success_message))

        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")

        return result