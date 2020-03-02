from flask_restx import Resource

from .service import ProjectService
from .dto import ProjectDto

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
