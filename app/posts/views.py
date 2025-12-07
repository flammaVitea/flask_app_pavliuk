from flask import render_template, abort
from . import post_bp


# Simple in-memory posts list for scaffold/demo
posts = [
    {'id': 1, 'title': 'First post', 'body': 'Content of first post.'},
    {'id': 2, 'title': 'Second post', 'body': 'Content of second post.'},
]

@post_bp.route('/posts')
def index():
    return render_template('posts/posts.html', posts=posts)


@post_bp.route('/<int:post_id>')
def detail(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        abort(404)
    return render_template('posts/detail_post.html', post=post)
