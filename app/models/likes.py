from datetime import datetime
from app import db

# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


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
