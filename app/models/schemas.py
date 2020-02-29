# Model Schemas
from app import ma

from .user import User
from .content import Project


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

        # Fields to expose.
        fields = ("email", "name", "username", "joined_date", "role_id")


class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project

        # Fields to expose.
        fields = ("public_id", "title", "content", "description")
