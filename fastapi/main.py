import requests
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from instrument import instrument_app

app = FastAPI()
instrument_app(app)
templates = Jinja2Templates(directory='templates')

@app.get('/')
def get_root(request: Request):
    return templates.TemplateResponse('form.html', {'request': request})

@app.post('/submit')
def submit_post(title: str = Form(...), text: str = Form(...)):
    post_data = {
        'title': title,
        'text': text
    }
    response = requests.post('http://flask-api:8001/submit', data=post_data)
    if response.status_code == 200:
        return "Post created!"
    return "Failed to create Post"


@app.get('/posts')
def view_posts(request: Request):
    response = requests.get("http://flask-api:8001/posts_raw")
    if response.status_code == 200:
        posts = response.json()
        return templates.TemplateResponse('posts.html', {'request': request, 'posts': posts})
    return "Failed to retrieve posts"

