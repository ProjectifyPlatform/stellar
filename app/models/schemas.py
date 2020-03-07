# Model Schemas
from app import ma

from .user import User
from .content import Project, Rating, Post, Comment


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

        # Fields to expose.
        fields = ("email", "name", "username", "bio", "joined_date", "role", "posts")


class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project

        # Fields to expose.
        fields = (
            "public_id",
            "title",
            "difficulty",
            "time_required",
            "abstract",
            "objective",
            "safety",
            "content",
            "created",
        )


class RatingSchema(ma.ModelSchema):
    class Meta:
        model = Rating

        # Fields to expose.
        fields = ("rating", "feedback", "rated_on")


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

        # Fields to expose.
        fields = ("public_id", "caption", "project", "comments", "created")


class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment

        # Fields to expose.
        fields = ("body", "created", "replies")
