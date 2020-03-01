from uuid import uuid4
from app.models.content import Project
from app.models.schemas import ProjectSchema

from tests.utils.base import BaseTestCase


class TestProjectModel(BaseTestCase):
    def test_public_id_are_random(self):
        p = Project(public_id=str(uuid4().int)[:15])
        p2 = Project(public_id=str(uuid4().int)[:15])

        self.assertNotEquals(p, p2)

    def test_schema(self):
        p = Project(content="lorem")
        p_dump = ProjectSchema().dump(p)

        self.assertEquals(p_dump["content"], "lorem")
