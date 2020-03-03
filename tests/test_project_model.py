from uuid import uuid4
from app.models.content import Project
from app.models.schemas import ProjectSchema

from tests.utils.base import BaseTestCase


class TestProjectModel(BaseTestCase):
    def test_public_ids_are_random(self):
        """ Check if project public IDs are random """
        p = Project(public_id=str(uuid4().int)[:15])
        p2 = Project(public_id=str(uuid4().int)[:15])

        self.assertNotEquals(p, p2)

    def test_schema(self):
        """ Check Project Schema output """
        content = "lorem"
        p = Project(content=content)
        p_dump = ProjectSchema().dump(p)

        self.assertEquals(p_dump["content"], content)
