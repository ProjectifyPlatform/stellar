from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.content import Project

from .utils import load_data, create_and_load


class ProjectService:
    @staticmethod
    def get_data(public_id):
        """ Get Project data by its public id """
        if not (project := Project.query.filter_by(public_id=public_id).first()):
            return err_resp("Project not found!", "project_404", 404)

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
        title = data["title"]
        difficulty = data["difficulty"]
        time_required = data["time_required"]

        abstract = data["abstract"]
        objective = data["objective"]
        safety = data.get("safety")
        content = data["content"]

        # Check if current_user is a creator.
        from app.models.user import Permission

        if not current_user.has_role(Permission.CREATE):
            return err_resp("User is not a creator.", "user_not_creator", 403)

        # Create a new project
        from uuid import uuid4

        try:
            project = Project(
                public_id=str(uuid4().int)[:15],
                creator_id=current_user.id,
                title=title,
                difficulty=difficulty,
                time_required=time_required,
                abstract=abstract,
                objective=objective,
                safety=safety,
                content=content,
            )

            project_data = create_and_load(project)

            resp = message(True, "Project created.")
            resp["project"] = project_data
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp
