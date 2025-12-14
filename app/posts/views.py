from flask import render_template, request, redirect, url_for, flash, abort
from . import post_bp
from app import db
from app.posts.models import Post
from app.posts.forms import PostForm
from app.users.models import User

@post_bp.route('/', methods=['GET'])
def index():
    """ відображення списку всіх видимих постів """
    posts = db.session.scalars(
        db.select(Post)
        .where(Post.is_active == True)
        .order_by(Post.posted.desc())
    ).all()
    return render_template('posts/posts.html', posts=posts)

@post_bp.route('/<int:id>', methods=['GET'])
def detail(id):
    """ перегляд конкретного поста """
    post = db.get_or_404(Post, id)
    return render_template('posts/detail_post.html', post=post)

@post_bp.route('/create', methods=['GET', 'POST'])
def create():
    """ створення поста """
    form = PostForm()
    
    form.author_id.choices = [(user.id, user.username) for user in db.session.query(User).all()]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data  
        )
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.index'))
    
    return render_template('posts/add_post.html', form=form, legend="Створити пост")

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    """ редагування поста """
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    form.author_id.choices = [(user.id, user.username) for user in db.session.query(User).all()]

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        
        post.user_id = form.author_id.data
        
        db.session.commit()
        flash('Пост оновлено!', 'success')
        return redirect(url_for('posts.detail', id=post.id))

    return render_template('posts/add_post.html', form=form, legend="Редагувати пост")

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост видалено!', 'info')
        return redirect(url_for('posts.index'))
        
    return render_template('posts/delete_confirm.html', post=post)