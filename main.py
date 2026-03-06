from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
    {"id": 1, "author": "Alice", "title": "First Post", "content": "This is the first post.", "data_posted": "2024-06-01T12:00:00Z"},
    {"id": 2, "author": "Bob", "title": "Second Post", "content": "This is the second post.", "data_posted": "2024-06-02T12:00:00Z"},
    {"id": 3, "author": "Charlie", "title": "Third Post", "content": "This is the third post.", "data_posted": "2024-06-03T12:00:00Z"},
    {"id": 4, "author": "Diana", "title": "Fourth Post", "content": "This is the fourth post.", "data_posted": "2024-06-04T12:00:00Z"},
    {"id": 5, "author": "Eve", "title": "Fifth Post", "content": "This is the fifth post.", "data_posted": "2024-06-05T12:00:00Z"}
]

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Welcome to the API</h1>"

@app.get("/api/posts", response_class=HTMLResponse)
def get_posts():
    return "<br>".join([f"{post['id']}: {post['title']} by {post['author']} (Posted on {post['data_posted']})" for post in posts])