from app import db


def load_posts_data(posts):
    """ Load many posts data """
    from app.models.schemas import PostSchema

    posts_schema = PostSchema(many=True)

    data = posts_schema.dump(posts)

    return data


def load_projects_data(projects):
    """ Load many projects data """
    from app.models.schemas import ProjectSchema

    projects_schema = ProjectSchema(many=True)

    data = projects_schema.dump(projects)

    return data


def load_page_data(pagination_obj):
    return dict(
        # Total number of pages
        total=pagination_obj.pages,
        # Has a next page
        has_next=pagination_obj.has_next,
        # Current page number
        current=pagination_obj.page,
        # Next page number,
        next=pagination_obj.next_num,
    )
