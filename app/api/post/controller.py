from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import validation_error

# Project modules
from .service import PostService
from .dto import PostDto
from .utils import CreatePost, UpdatePost

from ..user.utils import get_user

api = PostDto.api

# Define models/validators.
_success_response = PostDto.success_response

_create_validator = CreatePost()
_update_validator = UpdatePost()


@api.route("/<string:public_id>")
class Post(Resource):
    # Get
    @api.doc(
        responses={
            200: ("Post data successfully sent.", _success_response),
            404: "Post not found!",
        }
    )
    def get(self, public_id):
        """ Get a specific post's data using its public id """
        return PostService.get_data(public_id)

    # Update
    _update_model = PostDto.update_post

    @api.doc(
        responses={200: "Post has been updated.", 401: "Insufficient permissions.",},
    )
    @jwt_required
    @api.expect(_update_model, validate=True)
    def put(self, public_id):
        """ Update a post by its public id """
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        # Validate data
        if (errors := _update_validator.validate(data)) :
            return validation_error(False, errors), 400

        return PostService.update(data, public_id, current_user)

    # Delete
    @api.doc(
        responses={
            200: "Post has been deleted.",
            401: "Insufficient permissions.",
            404: "Post not found.",
        }
    )
    @jwt_required
    def delete(self, public_id):
        """ Delete a post using its public id """
        current_user = get_user(get_jwt_identity())

        return PostService.delete(public_id, current_user)


@api.route("/create/<string:project_public_id>")
class PostCreate(Resource):

    _create_model = PostDto.create_post

    @api.doc(
        responses={
            201: ("Post created.", _success_response),
            404: "Can't create post without project.",
        }
    )
    @api.expect(_create_model, validate=True)
    @jwt_required
    def post(self, project_public_id):
        """ Create a new post. """
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        # Validate data
        if (errors := _create_validator.validate(data)) :
            return validation_error(False, errors), 400

        return PostService.create(data, project_public_id, current_user)
