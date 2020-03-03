from datetime import datetime
from app import db

# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


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

    # Text values.
    abstract = Column(db.Text)
    objective = Column(db.Text)
    safety = Column(db.Text)
    content = Column(db.Text)

    created = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Project '{self.public_id}'>"


class Rating(Model):
    """
    Rating model for storing ratings of a project
    """

    id = Column(db.Integer, primary_key=True)
    rater_id = Column(db.Integer, db.ForeignKey("user.id"))
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

    # Relationships
    project = Column(db.String(15))
    comments = relationship("Comment", backref="post", lazy="dynamic")

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
    created = Column(db.DateTime, default=datetime.utcnow)
