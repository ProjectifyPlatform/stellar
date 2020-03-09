from flask_restx import Namespace, fields


class ProjectDto:

    api = Namespace("project", description="Project related operations.")

    project_obj = api.model(
        "Project object",
        {
            "public_id": fields.String,
            "title": fields.String,
            "difficulty": fields.Integer,
            "time_required": fields.String,
            "abstract": fields.String,
            "objective": fields.String,
            "safety": fields.String,
            "content": fields.String,
            "created": fields.DateTime,
        },
    )

    success_response = api.model(
        "Project success response",
        {
            "success": fields.Boolean,
            "message": fields.String,
            "project": fields.Nested(project_obj),
        },
    )

    project_create = api.model(
        "Project create",
        {
            "title": fields.String(required=True),
            "difficulty": fields.Integer(required=True),
            "time_required": fields.String(required=True),
            # Text values.
            "abstract": fields.String(required=True),
            "objective": fields.String(required=True),
            "safety": fields.String,
            "content": fields.String(required=True),
        },
    )

    update_model = api.model(
        "Project update model",
        {
            "title": fields.String,
            "abstract": fields.String,
            "objective": fields.String,
            "content": fields.String,
            "safety": fields.String,
            "content": fields.String,
        },
    )
