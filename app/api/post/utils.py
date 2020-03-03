def load_data(post_db_obj):
    """ Load post's data """
    from app.models.schemas import PostSchema

    post_schema = PostSchema()

    data = post_schema.dump(post_db_obj)

    return data
