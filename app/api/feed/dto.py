from flask_restx import Namespace


class FeedDto:

    api = Namespace("feed", description="Interact with projects/posts.")
