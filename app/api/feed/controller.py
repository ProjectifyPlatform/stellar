from flask import request
from flask_restx import Resource

# Project modules
from .service import FeedService
from .dto import FeedDto

api = FeedDto.api


@api.route("/posts")
class FeedPosts(Resource):
    # Get posts
    def get(self):
        page = request.args.get("page", 1, type=int)
        return FeedService.get_posts(page)


@api.route("/projects")
class FeedProjects(Resource):
    # Get projects
    def get(self):
        page = request.args.get("page", 1, type=int)
        category = request.args.get("category", None, type=str)
        return FeedService.get_projects(page, category)
