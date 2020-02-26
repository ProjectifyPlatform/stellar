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
    - TBA
    """
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    author_id = Column(db.Integer, db.ForeignKey("user.id"))

    title = Column(db.String(255))
    content = Column(db.Text)

    def get_creator_public_id(self):
        return self.author_id.public_id

    def __repr__(self):
        return f"<Project '{self.public_id}'>"
