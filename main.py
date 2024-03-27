from fastapi import FastAPI
from src.authentication.auth import router as auth_router
from src.Blog.blog import router as blog_router
from src.Blog_rating.blog_rating import router as rating_router
from src.BlogTag.admin_blog_tag import router as tag_router
from src.BlogTag.user_blog_tag import router as user_tag_router
from src.Comments.comment import router as comments_router
from src.Likes.likes import router as likes_router
from src.Shares.shares import router as shares_router
from src.Follows.follows import router as follows_router
from src.Users.users import router as user_router
from src.Search.search import router as search_router


def create_app(env: str = "dev") -> FastAPI:

    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(blog_router)
    app.include_router(rating_router)
    app.include_router(tag_router)
    app.include_router(user_tag_router)
    app.include_router(comments_router)
    app.include_router(likes_router)
    app.include_router(shares_router)
    app.include_router(follows_router)
    app.include_router(search_router)


if __name__ == "__main__":
    app = create_app()
