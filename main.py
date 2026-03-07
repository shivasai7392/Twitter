from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {"id": 1, "author": "Alice", "title": "First Post", "content": "This is the first post.", "date_posted": "2024-06-01T12:00:00Z"},
    {"id": 2, "author": "Bob", "title": "Second Post", "content": "This is the second post.", "date_posted": "2024-06-02T12:00:00Z"},
    {"id": 3, "author": "Charlie", "title": "Third Post", "content": "This is the third post.", "date_posted": "2024-06-03T12:00:00Z"},
    {"id": 4, "author": "Diana", "title": "Fourth Post", "content": "This is the fourth post.", "date_posted": "2024-06-04T12:00:00Z"},
    {"id": 5, "author": "Eve", "title": "Fifth Post", "content": "This is the fifth post.", "date_posted": "2024-06-05T12:00:00Z"}
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def get_posts(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "title": "Home"})