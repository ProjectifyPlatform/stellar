from datetime import datetime
from app import db

# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Category(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True)
    description = Column(db.String(512))
    projects = relationship("Project", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name}>"


class Project(Model):
    """
    Projects model for storing project related details

    Relationships:
    - Ratings

    Difficulties:
    0 - Easy, 1 - Normal, 2 - Medium,
    3 - Hard, 4 - Advanced, 5 - Unspecified.
    """

    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    creator_id = Column(db.Integer, db.ForeignKey("user.id"))

    title = Column(db.String(255))
    difficulty = Column(db.Integer)
    time_required = Column(db.String(20))
    image_hash = Column(db.String(40))

    # Text values.
    abstract = Column(db.Text)
    objective = Column(db.Text)
    safety = Column(db.Text)
    content = Column(db.Text)

    created = Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    ratings = relationship("Rating", backref="project", lazy="dynamic")
    posts = relationship("Post", backref="project", lazy="dynamic")
    category_id = Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        return f"<Project '{self.public_id}'>"


class Rating(Model):
    """
    Rating model for storing ratings of a project
    """

    id = Column(db.Integer, primary_key=True)
    # The user that created this rating.
    rater_id = Column(db.Integer, db.ForeignKey("user.id"))
    on_project = Column(db.Integer, db.ForeignKey("project.id"))
    # Whole numbers only (0 - 5)
    rating = Column(db.Integer)
    feedback = Column(db.Text)

    rated_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Rating '{self.id}'>"


class Post(Model):
    """
    Post model for storing post related details

    Relationships:
    - Project
    - Comments
    - Likes
    """

    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    author_id = Column(db.Integer, db.ForeignKey("user.id"))
    caption = Column(db.Text)
    image_hash = Column(db.String(40))

    # Relationships
    on_project = Column(db.Integer, db.ForeignKey("project.id"))
    comments = relationship("Comment", backref="post", lazy="dynamic")
    likes = relationship(
        "PostLike", backref="post", cascade="all, delete-orphan", lazy="dynamic"
    )

    created = Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post '{self.public_id}'>"


class Comment(Model):
    """
    Comment model for storing comment related details

    Relationships:
    - on_post
    - Likes
    """

    id = Column(db.Integer, primary_key=True)
    author_id = Column(db.Integer, db.ForeignKey("user.id"))
    on_post = Column(db.Integer, db.ForeignKey("post.id"))

    body = Column(db.Text)
    likes = relationship("CommentLike", backref="comment", lazy="dynamic")

    created = Column(db.DateTime, default=datetime.utcnow)


# Likes
class PostLike(Model):
    """ PostLike Model for storing post like related details """

    # Details
    id = Column(db.Integer, primary_key=True)
    on_post = Column(db.Integer, db.ForeignKey("post.id"))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"))
    liked_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PostLike '{self.id}'>"


class CommentLike(Model):
    """ CommentLike Model for storing comment like related details """

    # Details
    id = Column(db.Integer, primary_key=True)
    on_comment = Column(db.Integer, db.ForeignKey("comment.id"))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"))
    liked_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CommentLike '{self.id}'>"
