from flask_restx import Namespace, fields


class PostDto:

    api = Namespace("post", description="User created posts.")

    post_obj = api.model(
        "Post object",
        {
            "public_id": fields.String,
            "caption": fields.String,
            "image_hash": fields.String,
            "comments": fields.Nested,
        },
    )
