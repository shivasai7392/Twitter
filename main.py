"""FastAPI Twitter clone - blog with posts and API endpoints."""

from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

import models
from database import Base, engine, get_db
from schemas import PostCreate, PostResponse, UserCreate, UserResponse

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Alice",
        "title": "First Post",
        "content": "This is the first post.",
        "date_posted": datetime(2024, 6, 1, 12, 0, 0),
    },
    {
        "id": 2,
        "author": "Bob",
        "title": "Second Post",
        "content": "This is the second post.",
        "date_posted": datetime(2024, 6, 2, 12, 0, 0),
    },
    {
        "id": 3,
        "author": "Charlie",
        "title": "Third Post",
        "content": "This is the third post.",
        "date_posted": datetime(2024, 6, 3, 12, 0, 0),
    },
    {
        "id": 4,
        "author": "Diana",
        "title": "Fourth Post",
        "content": "This is the fourth post.",
        "date_posted": datetime(2024, 6, 4, 12, 0, 0),
    },
    {
        "id": 5,
        "author": "Eve",
        "title": "Fifth Post",
        "content": "This is the fifth post.",
        "date_posted": datetime(2024, 6, 5, 12, 0, 0),
    },
]


# Posts Page routes
@app.get("/", include_in_schema=True, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def get_posts(request: Request, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Render the home page listing all posts."""
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "posts": [PostResponse.model_validate(post) for post in posts],
            "title": "Home",
        },
    )


@app.get("/posts/{post_id}", include_in_schema=False, name="post")
def get_post(
    post_id: int, request: Request, db: Annotated[Session, Depends(get_db)]
) -> Response:
    """Render a single post by id, or raise 404 if not found."""
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return templates.TemplateResponse(
            "post.html",
            {
                "request": request,
                "post": PostResponse.model_validate(post),
                "title": post.title,
            },
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

# User Page routes
@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    """Render a page listing all posts by a user."""
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = db.execute(select(models.Post).where(models.Post.author_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        "user_posts.html",
        {
            "request": request,
            "posts": [PostResponse.model_validate(post) for post in posts],
            "user": UserResponse.model_validate(user),
            "title": f"{user.username}'s Posts",
        },
    )

# Post API endpoints
@app.get("/api/posts", name="posts_api", response_model=list[PostResponse])
def get_posts_api(db: Annotated[Session, Depends(get_db)]) -> list[PostResponse]:
    """Return all posts as JSON."""
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return [PostResponse.model_validate(post) for post in posts]


@app.get("/api/posts/{post_id}", name="post_api", response_model=PostResponse)
def get_post_api(post_id: int, db: Annotated[Session, Depends(get_db)]) -> PostResponse:
    """Return a single post by id as JSON, or raise 404 if not found."""
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return PostResponse.model_validate(post)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post(
    "/api/posts",
    name="create_post_api",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    post: PostCreate, db: Annotated[Session, Depends(get_db)]
) -> PostResponse:
    """Create a new post and return it as JSON."""
    result = db.execute(select(models.User).where(models.User.id == post.author_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    new_post = models.Post(
        title=post.title, content=post.content, author_id=post.author_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return PostResponse.model_validate(new_post)


# User API endpoints
@app.get("/api/users/{user_id}", name="get_user_api", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> UserResponse:
    """Return a single user by id as JSON, or raise 404 if not found."""
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return UserResponse.model_validate(user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/api/users/{user_id}/posts",name="get_user_posts_api", response_model=list[PostResponse])
def get_user_posts(
    user_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[PostResponse]:
    """Return all posts by a user as JSON, or raise 404 if not found."""
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = db.execute(select(models.Post).where(models.Post.author_id == user_id))
    posts = result.scalars().all()
    return [PostResponse.model_validate(post) for post in posts]


@app.post(
    "/api/users",
    name="create_user_api",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    """Create a new user and return it as JSON."""
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    result = db.execute(select(models.User).where(models.User.email == user.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    new_user = models.User(
        username=user.username, password=user.password, email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.model_validate(new_user)


# Exception handlers
@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions: JSON for API routes, error.html for page routes."""
    message = exc.detail if exc.detail else "Something went wrong"

    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"error": message})
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_message": message,
        },
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
def custom_request_validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors: JSON for API routes, error.html for page routes."""
    message = "Invalid request data"

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exc.errors()},
        )
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_message": message,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
