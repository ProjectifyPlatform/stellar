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
    - Comments
    """

    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    author_id = Column(db.Integer, db.ForeignKey("user.id"))

    # Relationships
    comments = relationship("Comment", backref="project", lazy="dynamic")

    title = Column(db.String(255))
    content = Column(db.Text)
    description = Column(db.Text)
    created = Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"<Project '{self.public_id}'>"


class Comment(Model):
    """
    Comments model for storing comment related details

    Relationships:
    - Comments
    - Likes
    """

    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    author_id = Column(db.Integer, db.ForeignKey("user.id"))
    on_project = Column(db.Integer, db.ForeignKey("project.id"))

    # Comment body
    body = Column(db.Text)
    created = Column(db.DateTime, default=datetime.utcnow)
