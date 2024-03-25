from fastapi import FastAPI
from authentication.auth import router as auth_router
from Blog.blog import router as blog_router
from Blog_rating.blog_rating import router as rating_router
from BlogTag.admin_blog_tag import router as tag_router
from BlogTag.user_blog_tag import router as user_tag_router
from Comments.comment import router as comments_router
from Likes.likes import router as likes_router
from Shares.shares import router as shares_router
from Follows.follows import router as follows_router
from Users.users import router as user_router
from Search.search import router as search_router

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
