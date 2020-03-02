from flask_restx import Namespace, fields


class ProjectDto:

    api = Namespace("project", description="Project related operations.")
