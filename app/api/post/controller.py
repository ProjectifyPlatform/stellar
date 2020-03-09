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

    _create_model = PostDto.create_post

    @api.doc(
        responses={201: "Post created.", 404: "Can't create post without project."}
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


@api.route("/update/<string:public_id>")
class PostUpdate(Resource):

    _update_model = PostDto.update_post

    @api.doc(
        responses={200: "Post has been updated.", 401: "Insufficient permissions.",},
    )
    @jwt_required
    def put(self, public_id):
        """ Update a post using its public id """
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        return PostService.update(data, public_id, current_user)


@api.route("/delete/<string:public_id>")
class PostDelete(Resource):
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
