def load_data(project_db_obj):
    """ Load project's data """
    from app.models.schemas import ProjectSchema

    project_schema = ProjectSchema()

    data = project_schema.dump(project_db_obj)

    return data
