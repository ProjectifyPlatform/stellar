from flask import current_app
from app.utils import message, internal_err_resp

from app.models.content import Post, Project, Category
from .utils import load_page_data


class FeedService:
    @staticmethod
    def get_posts(page: int):
        from .utils import load_posts_data

        # Get posts from database.
        try:
            posts_query = Post.query.order_by(Post.created.desc()).paginate(
                page, current_app.config["POSTS_PER_PAGE"], False
            )

            posts_data = load_posts_data(posts_query.items)

            resp = message(True, "Posts data sent.")
            resp["page"] = load_page_data(posts_query)
            resp["posts"] = posts_data

            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_projects(page: int, category_name: str):
        from .utils import load_projects_data

        # Get projects from database.
        if not category_name:
            category_name = "science"

        try:
            category = Category.query.filter_by(name=category_name).first()

            projects_query = (
                Project.query.filter_by(category=category)
                .order_by(Project.created.desc())
                .paginate(page, current_app.config["PROJECTS_PER_PAGE"], False)
            )

            projects_data = load_projects_data(projects_query.items)

            resp = message(True, "Projects data sent.")
            resp["page"] = load_page_data(projects_query)
            resp["projects"] = projects_data

            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
