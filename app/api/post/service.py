from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.content import Post


class PostService:
    @staticmethod
    def get_data(public_id):
        """ Get Post data by its public id """
        if not (post := Post.query.filter_by(public_id=public_id).first()):
            return err_resp("Post not found!", "post_404", 404)

        from .utils import load_data

        try:
            post_data = load_data(post)

            resp = message(True, "Post data succcessfully sent.")
            resp["post"] = post_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
