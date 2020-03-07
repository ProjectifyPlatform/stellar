from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import validation_error

# Project modules
from .service import ProjectService
from .dto import ProjectDto
from .utils import CreateProject

from ..user.utils import get_user

api = ProjectDto.api

# Define models/validators.
_project_success = ProjectDto.project_success
_create_model = ProjectDto.project_create

_create_validator = CreateProject()


@api.route("/get/<string:public_id>")
class ProjectGet(Resource):
    @api.doc(
        responses={
            200: ("Project data successfully sent", _project_success),
            404: "Project not found!",
        },
    )
    def get(self, public_id):
        """ Get a specific project's data by its public id """
        return ProjectService.get_data(public_id)


@api.route("/create")
class ProjectCreate(Resource):
    @api.doc(
        responses={
            201: ("Project data successfully created.", _project_success),
            403: "User is not a creator.",
        },
    )
    @api.expect(_create_model, validate=True)
    @jwt_required
    def post(self):
        """ Create a new project. """
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        # Validate data
        if (errors := _create_validator.validate(data)) :
            return validation_error(False, errors), 400

        return ProjectService.create(data, current_user)


@api.route("/delete/<string:public_id>")
class ProjectDelete(Resource):
    @api.doc(
        responses={200: "Project has been deleted.", 401: "Insufficient permissions."},
    )
    @jwt_required
    def delete(self, public_id):
        """ Delete a specific project from the DB using its public id """
        current_user = get_user(get_jwt_identity())
        return ProjectService.delete(public_id, current_user)
