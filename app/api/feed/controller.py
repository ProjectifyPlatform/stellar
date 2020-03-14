from flask import request
from flask_restx import Resource

# Project modules
from .service import FeedService
from .dto import FeedDto

api = FeedDto.api

# Define models
_posts_success_response = FeedDto.posts_success_response
_projects_success_response = FeedDto.projects_success_response


@api.route("/posts")
class FeedPosts(Resource):
    @api.doc(
        responses={200: ("Post data successfully sent.", _projects_success_response),}
    )
    def get(self):
        page = request.args.get("page", 1, type=int)
        return FeedService.get_posts(page)


@api.route("/projects")
class FeedProjects(Resource):
    @api.doc(
        responses={200: ("Post data successfully sent.", _projects_success_response),}
    )
    def get(self):
        page = request.args.get("page", 1, type=int)
        category = request.args.get("category", None, type=str)
        return FeedService.get_projects(page, category)
