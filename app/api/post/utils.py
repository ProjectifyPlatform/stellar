from app import db


def load_data(post_db_obj):
    """ Load post's data """
    from app.models.schemas import PostSchema

    post_schema = PostSchema()

    data = post_schema.dump(post_db_obj)

    return data


def create_and_load(post_obj):
    db.session.add(post_obj)
    db.session.flush()

    data = load_data(post_obj)

    db.session.commit()

    return data


def delete_post(post_db_obj):
    db.session.delete(post_db_obj)
    db.session.commit()

    return True


# Validations with Marshmallow
from marshmallow import Schema, fields
from marshmallow.validate import Length


class CreatePost(Schema):
    """ /api/post/create/<string:project_public_id> [POST]

    Parameters:
    - Caption (Str)
    - Image Hash (Str)
    """

    caption = fields.Str(required=True, validate=[Length(min=1, max=2200)])
    image_hash = fields.Str(validate=[Length(min=30)])


class UpdatePost(Schema):
    """ /api/post/<string:public_id>

    Parameters:
    - Caption (Str)
    """

    caption = fields.Str(required=True, validate=[Length(min=1, max=2200)])
