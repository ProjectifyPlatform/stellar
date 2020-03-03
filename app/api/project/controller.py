from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from .service import ProjectService
from .dto import ProjectDto

from ..user.utils import get_user

api = ProjectDto.api


@api.route("/get/<string:public_id>")
class ProjectGet(Resource):
    @api.doc(
        "Get a specific project",
        responses={200: "Project data successfully sent", 404: "Project not found!",},
    )
    def get(self, public_id):
        """ Get a specific project's data by its public id """
        return ProjectService.get_data(public_id)


@api.route("/")
class ProjectCreate(Resource):
    @api.doc(
        "Create a new project",
        responses={
            201: "Project data successfully created.",
            403: "User is not a creator.",
        },
    )
    @jwt_required
    def post(self):
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        return ProjectService.create(data, current_user)
