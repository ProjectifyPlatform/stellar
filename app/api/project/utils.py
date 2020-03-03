def load_data(project_db_obj):
    """ Load project's data """
    from app.models.schemas import ProjectSchema

    project_schema = ProjectSchema()

    data = project_schema.dump(project_db_obj)

    return data


# Validations with Marshmallow
from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp, Range


class CreateSchema(Schema):
    """ /project/create [POST]

    Parameters:
    - Title
    - Difficulty
    - Time Required

    -- db.Text
    - Abstract
    - Objective
    - Safety
    - Content
    """

    title = fields.Str(required=True, validate=[Length(min=2, max=128)])
    difficulty = fields.Int(required=True, validate=[Range(min=0, max=5)])
    time_required = fields.Str(required=True, validate=[Length(max=20)])

    # Text values.
    abstract = fields.Str(required=True)
    objective = fields.Str(required=True)
    safety = fields.Str()
    content = fields.Str(required=True)
