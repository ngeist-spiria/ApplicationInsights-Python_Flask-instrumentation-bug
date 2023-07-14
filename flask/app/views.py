from flask import Blueprint, jsonify, render_template, request
import requests

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def create_post_form():
    return render_template('form.html')

@index_bp.route('/submit', methods=["POST"])
def submit_post():
    title = request.form.get('title')
    text = request.form.get('text')
    post_data = {
        'title': title,
        'text': text
    }
    response = requests.post('http://django-api:8000/api/posts/', data=post_data)
    if response.status_code == 201:
        return jsonify(message=f'Created post with ID {response.content}')
    return jsonify(message=f'Failed to create post')


@index_bp.route('/posts')
def view_posts():
    response = requests.get('http://django-api:8000/api/posts/')
    if response.status_code == 200:
        posts = response.json()
        return render_template('posts.html', posts=posts)
    return jsonify(message=f'Failed to retrieve posts')


@index_bp.route('/posts_raw')
def view_posts_raw():
    header_val = request.headers.get('traceparent')
    print(header_val)
    response = requests.get('http://django-api:8000/api/posts/')
    if response.status_code == 200:
        posts = response.json()
        return posts
    return jsonify(message=f'Failed to retrieve posts')