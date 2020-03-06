from flask_restx import Namespace, fields

from ..project.dto import ProjectDto

project_obj = ProjectDto.project_obj


class UserDto:

    api = Namespace("user", description="User related operations.")
    user = api.model(
        "User object",
        {
            "public_id": fields.String,
            "email": fields.String,
            "username": fields.String,
            "name": fields.String,
            "projects": fields.List(fields.Nested(project_obj)),
            "joined_date": fields.DateTime,
            "role_id": fields.Integer,
        },
    )

    data_resp = api.model(
        "User Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "user": fields.Nested(user),
        },
    )
