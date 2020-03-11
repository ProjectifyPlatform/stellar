from flask import request
from flask_restx import Resource

# Project modules
from .dto import FeedDto

api = FeedDto.api


@api.route("/")
class Feed(Resource):
    # Get
    def get(self):
        page = request.args.get("page", 1, type=int)
        # Implement feed service for getting posts/projects chronologically.
        pass
