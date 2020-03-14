from flask_restx import Namespace, fields

from ..post.dto import PostDto
from ..project.dto import ProjectDto

post_obj = PostDto.post_obj
project_obj = ProjectDto.project_obj


class FeedDto:

    api = Namespace("feed", description="Interact with projects/posts.")

    page_obj = api.model(
        "Page data object",
        {
            "total": fields.Integer,
            "has_next": fields.Boolean,
            "current": fields.Integer,
            "next": fields.Integer,
        },
    )

    posts_success_response = api.model(
        "Posts get success response",
        {
            "success": fields.Boolean,
            "message": fields.String,
            "page": fields.Nested(page_obj),
            "posts": fields.List(fields.Nested(post_obj)),
        },
    )

    projects_success_response = api.model(
        "Projects get success response",
        {
            "success": fields.Boolean,
            "message": fields.String,
            "page": fields.Nested(page_obj),
            "posts": fields.List(fields.Nested(project_obj)),
        },
    )
