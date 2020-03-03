from uuid import uuid4
from app.models.content import Post
from app.models.schemas import PostSchema

from tests.utils.base import BaseTestCase


class TestPostModel(BaseTestCase):
    def test_public_ids_are_random(self):
        """ Check if post public IDs are random """
        p = Post(public_id=str(uuid4().int)[:15])
        p2 = Post(public_id=str(uuid4().int)[:15])

        self.assertNotEquals(p, p2)

    def test_schema(self):
        """ Check Post Schema output """
        caption = "lorem"
        p = Post(caption=caption)
        p_dump = PostSchema().dump(p)

        self.assertEquals(p_dump["caption"], caption)
