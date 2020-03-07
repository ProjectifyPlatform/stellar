def get_user(id):
    from app.models.user import User

    u = User.query.get(id)

    return u


def load_data(user_db_obj):
    """ Load user's data """
    from app.models.schemas import UserSchema

    user_schema = UserSchema()

    data = user_schema.dump(user_db_obj)

    return data


# Validation with Marshmallow
from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp


class UserUpdate(Schema):
    """ /api/user/update [PUT]

    Parameters:
    - Username (Str)
    - Bio (Str)
    """

    username = fields.Str(
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid username!",
            ),
        ],
    )

    bio = fields.Str(validate=[Length(min=1, max=150),])
