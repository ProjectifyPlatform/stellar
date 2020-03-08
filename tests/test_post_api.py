import json
from flask_jwt_extended import create_access_token

from app import db
from app.models.content import Post

from tests.utils.base import BaseTestCase


def get_post_data(self, public_id):
    return self.client.get(
        f"/api/post/get/{public_id}", content_type="application/json"
    )


class TestPostBlueprint(BaseTestCase):
    def test_post_get(self):
        """ Test getting a post from DB """
        data = dict(caption="Brogramming", public_id=123)
        post = Post(caption=data["caption"], public_id=data["public_id"])

        db.session.add(post)
        db.session.commit()

        post_resp = get_post_data(self, data["public_id"])
        post_data = json.loads(post_resp.data.decode())

        self.assertTrue(post_resp.status)
        self.assertEqual(post_resp.status_code, 200)
        self.assertEqual(post_data["post"]["caption"], data["caption"])

        # Test a 404 request
        post_404_resp = get_post_data(self, 69)
        self.assertEqual(post_404_resp.status_code, 404)

    def test_post_create(self):
        """ Test post creation """
        data = dict(caption="A caption.", image_hash=123321,)
