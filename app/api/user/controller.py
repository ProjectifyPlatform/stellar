from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import validation_error

from .service import UserService
from .dto import UserDto
from .utils import UserUpdate, get_user

api = UserDto.api
data_resp = UserDto.data_resp

# Define models/validators
_update_model = UserDto.update_user

_update_validator = UserUpdate()


@api.route("/get/<string:username>")
class UserGet(Resource):
    @api.doc(
        responses={
            200: ("User data successfully sent", data_resp),
            404: "User not found!",
        },
    )
    def get(self, username):
        """ Get a specific user's data by their username """
        return UserService.get_data(username)


@api.route("/update")
class UserUpdate(Resource):
    @api.doc(
        responses={
            200: "User has been updated.",
            204: "No data provided, nothing to do.",
            400: "Validations failed",
        },
    )
    @api.expect(_update_model, validate=True)
    @jwt_required
    def put(self):
        data = request.get_json()
        current_user = get_user(get_jwt_identity())

        # Validate
        if (errors := _update_validator.validate(data)) :
            return validation_error(False, errors), 400

        return UserService.update_data(data, current_user)
