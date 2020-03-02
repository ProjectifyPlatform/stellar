from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.content import Project


class ProjectService:
    @staticmethod
    def get_data(public_id):
        """ Get Project data by its public id """
        if not (project := Project.query.filter_by(public_id=public_id).first()):
            return err_resp("Project not found!", "project_404", 404)

        from .utils import load_data

        try:
            project_data = load_data(project)

            resp = message(True, "Project data sent")
            resp["project"] = project_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def create(data, current_user):
        # Assign the vars

        # Check if current_user is a creator.

        return
