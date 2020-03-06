from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import validation_error

# Project modules
from .service import PostService
from .dto import PostDto
from .utils import CreatePost

from ..user.utils import get_user

api = PostDto.api

_create_validator = CreatePost()


@api.route("/get/<string:public_id>")
class PostGet(Resource):
    @api.doc(responses={200: "Post data sent.", 404: "Post not found!"})
    def get(self, public_id):
        """ Get a specific post's data using its public id """
        return PostService.get_data(public_id)


@api.route("/create/<string:project_public_id>")
class PostCreate(Resource):

    # Create new post
    _create_post = PostDto.create_post

    @api.doc(
        responses={201: "Post created.", 404: "Can't create post without project."}
    )
    @api.expect(_create_post, validate=True)
    @jwt_required
    def post(self, project_public_id):
        """ Create a new post. """
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        # Validate data
        if not (errors := _create_validator.validate(data)):
            return validation_error(False, errors), 400

        return PostService.create(data, project_public_id, current_user)
