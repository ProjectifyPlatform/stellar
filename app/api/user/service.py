from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.user import User


class UserService:
    @staticmethod
    def get_data(username):
        """ Get user data by username """
        if not (user := User.query.filter_by(username=username).first()):
            return err_resp("User not found!", "user_404", 404)

        from .utils import load_data

        try:
            user_data = load_data(user)

            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_data(data, user):

        if not data:
            return message(True, "Nothing to update."), 204

        try:
            from app import db

            if (username := data.get("username")) :
                user.username = username

            if (bio := data.get("bio")) :
                user.bio = bio

            # Commit changes to db.
            db.session.commit()

            return message(True, "User data updated."), 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
