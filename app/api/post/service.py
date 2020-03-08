from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.content import Post, Project
from app.models.user import Permission


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

    @staticmethod
    def create(data, project_public_id, current_user):
        # Assign the vars
        caption = data["caption"]
        image_hash = data.get("image_hash")

        # Check if the project exists
        if not (
            project := Project.query.filter_by(public_id=project_public_id).first()
        ):
            return err_resp("Can't create post without project.", "project_404", 404)

        # Create a new post
        try:
            from uuid import uuid4
            from .utils import create_and_load

            post = Post(
                public_id=str(uuid4().int)[:15],
                author_id=current_user.id,
                caption=caption,
                image_hash=image_hash,
                on_project=project.id,
            )

            post_data = create_and_load(post)

            resp = message(True, "Post created.")
            resp["post"] = post_data
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def delete(public_id, current_user):
        if not (post := Post.query.filter_by(public_id=public_id).first()):
            return err_resp("Post not found.", "project_404", 404)

        # Check if the current user is the owner/admin/moderator.
        if (
            post.author.public_id == current_user.public_id
            or current_user.has_role(Permission.MODERATE)
            or current_user.has_role(Permission.ADMIN)
        ):
            try:
                from .utils import delete_post

                delete_post(post)

                resp = message(True, "Post deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return internal_err_resp()

        return err_resp("Insufficient permissions!", "user_unauthorized", 401)

    @staticmethod
    def update(data, public_id, current_user):
        if not (post := Post.query.filter_by(public_id).first()):
            return err_resp("Post not found.", "post_404", 404)

        # Check if the current user is the owner.
        if post.author.public_id == current_user.public_id:
            try:
                from app import db

                if (caption := data.get("caption")) :
                    post.caption = caption

                # Commit changes to db.
                db.session.commit()

                return message(True, "Post data updated"), 200

            except Exception as error:
                current_app.logger.error(error)
                return internal_err_resp()

        return err_resp("Insufficient permissions!", "user_unauthorized", 401)
