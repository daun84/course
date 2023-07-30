import flask
from flask import request, redirect, url_for, render_template, flash, session, g

from models.ModelUser import ModelUser
from models.ModelPost import ModelPost
from models.enums.EnumPostStatus import EnumPostStatus

from sqlalchemy import and_, func


class ControllerPosts:
    blueprint = flask.Blueprint("posts", __name__, url_prefix="/posts")

    @staticmethod
    @blueprint.route('/')
    def published_posts():
        all_posts = g.db_session.query(ModelPost).filter(
            ModelPost.post_status == EnumPostStatus.published
        ).all()
        return render_template('home.html', posts=all_posts)

    
    @staticmethod
    @blueprint.route('/new', methods=["POST", "GET"])
    def new():
        if g.user is None:
            return redirect(url_for('authentication.login'))

        # checking if current user has draft post 
        # (there can be only one draft post for user)
        post = g.db_session.query(ModelPost).filter(and_(
            ModelPost.post_status == EnumPostStatus.draft, 
            ModelPost.post_author_id == g.user.user_id
        )).first()

        if request.method == "POST":
            # if there's no draft post - creat new one
            if post is None:
                post = ModelPost()
                post.post_status = EnumPostStatus.draft
                post.post_author = g.user
                g.db_session.add(post)

            post.post_title = request.form.get('title').strip()
            post.post_body = request.form.get('body').strip()
            g.db_session.commit()
            

            url_slug = request.form.get('url_slug').strip()

            action = request.form.get('action')

            if 'draft' == action:
                post.post_url_slug = url_slug
                g.db_session.commit()
                return redirect(url_for('posts.published_posts'))
            elif 'publish' == action:
                # check if url_slug is compatible 
                existing_post = g.db_session.query(ModelPost).filter(and_(
                    ModelPost.post_url_slug == url_slug,
                    ModelPost.post_id != post.post_id
                    )).first()

                if ' ' in url_slug:
                    flash("This url_slug is not allowed", category='error')
                elif existing_post:
                    flash("This url_slug is already being used", category='error')
                else:
                    post.post_url_slug = url_slug
                    post.post_status = EnumPostStatus.published
                    post.post_created = func.now()
                    g.db_session.commit()
                    return redirect(url_for('posts.published_posts'))

        return render_template('new_post.html', post=post)

    @staticmethod
    @blueprint.route('/edit/<url_slug>', methods=["POST", "GET"])
    def edit(url_slug):
        post = g.db_session.query(ModelPost).filter(and_(
            ModelPost.post_status == EnumPostStatus.published, 
            ModelPost.post_url_slug == url_slug
        )).first()

        if post is None:
            return redirect(url_for('posts.published_posts'))
        elif g.user is not post.post_author:
            return redirect(url_for('authentication.login'))
        elif request.method == "POST":
                
            slug = request.form.get('url_slug').strip()

            action = request.form.get('action')

            if 'update' == action:
                existing_post = g.db_session.query(ModelPost).filter(and_(
                    ModelPost.post_url_slug == slug,
                    ModelPost.post_id != post.post_id
                )).first()

                if ' ' in slug:
                    flash("This url_slug is not allowed", category='error')
                elif existing_post:
                    flash("This url_slug is already being used", category='error')
                else:
                    post.post_title = request.form.get('title').strip()
                    post.post_body = request.form.get('body').strip()
                    post.post_url_slug = slug
                    post.post_modified = func.now()
                    g.db_session.commit()
                    return redirect(url_for('posts.published_posts'))
            elif 'delete' == action:
                post.post_status = EnumPostStatus.deleted
                g.db_session.commit()
                return redirect(url_for('posts.published_posts'))

        return render_template('edit_post.html', post=post)


    @staticmethod
    @blueprint.route('/view/<url_slug>')
    def view(url_slug):
        post = g.db_session.query(ModelPost).filter(and_(
            ModelPost.post_status == EnumPostStatus.published, 
            ModelPost.post_url_slug == url_slug
        )).first()

        if post is None:
            result = redirect(url_for('posts.published_posts'))
        else:
            result = render_template('view.html', post=post)

        return result