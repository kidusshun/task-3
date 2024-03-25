from sqlalchemy import Boolean, Column, ForeignKey, Integer, UUID, String, TIME
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/blog"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    name = Column(String)
    bio = Column(String)
    role = Column(String)
    createdAt = Column(TIME)
    updatedAt = Column(TIME)

    blogs = relationship("Blog", back_populates="owner")
    blog_ratings = relationship("BlogRatings", back_populates="user")
    comments = relationship("Comments", back_populates="user")
    Likes = relationship("Likes", back_populates="user")
    Shares = relationship("Shares", back_populates="user")

    followers = relationship(
        "Follows", foreign_keys="Follows.FollowedID", back_populates="followed"
    )
    following = relationship(
        "Follows", foreign_keys="Follows.FollowerID", back_populates="follower"
    )


class Blog(Base):
    __tablename__ = "blogs"

    blogID = Column(UUID, primary_key=True)
    userID = Column(UUID, ForeignKey("users.id"))
    title = Column(String)
    content = Column(String)

    createdAt = Column(TIME)
    updatedAt = Column(TIME)

    owner = relationship("User", back_populates="blogs")
    blog_ratings = relationship("BlogRatings", back_populates="blog")
    blog_tags = relationship("BlogTags", back_populates="blog")
    comments = relationship("Comments", back_populates="blog")
    Likes = relationship("Likes", back_populates="blog")
    Shares = relationship("Shares", back_populates="blog")


class BlogRatings(Base):
    __tablename__ = "blog_ratings"

    blogRatingID = Column(UUID, primary_key=True)
    userID = Column(UUID, ForeignKey("users.id"))
    blogID = Column(UUID, ForeignKey("blogs.blogID"))
    rating = Column(Integer)

    createdAt = Column(TIME)
    updatedAt = Column(TIME)

    blog = relationship("Blog", back_populates="blog_ratings")
    user = relationship("User", back_populates="blog_ratings")


class Tags(Base):
    __tablename__ = "tags"
    TagName = Column(String, unique=True, primary_key=True)
    createdAt = Column(TIME)
    updatedAt = Column(TIME)

    blog_tags = relationship("BlogTags", back_populates="tag")


class BlogTags(Base):
    __tablename__ = "blog_tags"

    BlogTagID = Column(UUID, primary_key=True)
    BlogID = Column(UUID, ForeignKey("blogs.blogID"))
    UserID = Column(UUID, ForeignKey("users.id"))
    TagName = Column(String, ForeignKey("tags.TagName"))

    createdAt = Column(TIME)
    updatedAt = Column(TIME)

    blog = relationship("Blog", back_populates="blog_tags")
    tag = relationship("Tags", back_populates="blog_tags")


class Comments(Base):
    __tablename__ = "comments"

    CommentID = Column(UUID, primary_key=True)
    UserID = Column(UUID, ForeignKey("users.id"))
    BlogID = Column(UUID, ForeignKey("blogs.blogID"))
    content = Column(String)

    CreatedAt = Column(TIME)
    UpdatedAt = Column(TIME)

    blog = relationship("Blog", back_populates="comments")
    user = relationship("User", back_populates="comments")


class Likes(Base):
    __tablename__ = "likes"

    LikeID = Column(UUID, primary_key=True)
    UserID = Column(UUID, ForeignKey("users.id"))
    BlogID = Column(UUID, ForeignKey("blogs.blogID"))

    CreatedAt = Column(TIME)
    UpdatedAt = Column(TIME)

    user = relationship("User", back_populates="Likes")
    blog = relationship("Blog", back_populates="Likes")


class Shares(Base):
    __tablename__ = "shares"

    ShareID = Column(UUID, primary_key=True)
    UserID = Column(UUID, ForeignKey("users.id"))
    BlogID = Column(UUID, ForeignKey("blogs.blogID"))

    CreatedAt = Column(TIME)
    UpdatedAt = Column(TIME)

    user = relationship("User", back_populates="Shares")
    blog = relationship("Blog", back_populates="Shares")


class Follows(Base):
    __tablename__ = "follows"

    FollowID = Column(UUID, primary_key=True)
    FollowerID = Column(UUID, ForeignKey("users.id"))
    FollowedID = Column(UUID, ForeignKey("users.id"))

    CreatedAt = Column(TIME)
    UpdatedAt = Column(TIME)

    follower = relationship(
        "User", foreign_keys=[FollowerID], back_populates="following"
    )
    followed = relationship(
        "User", foreign_keys=[FollowedID], back_populates="followers"
    )


def create_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    create_db()
