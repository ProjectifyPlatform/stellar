import json

from app import db
from app.models.content import Project

from tests.utils.base import BaseTestCase


def get_project_data(self, public_id):
    return self.client.get(
        f"/api/project/get/{public_id}", content_type="application/json",
    )


class TestProjectBlueprint(BaseTestCase):
    def test_project_get(self):
        """ Test getting a project from DB """
        data = dict(content="Brogramming",public_id=123)
        project = Project(content=data["content"], public_id=data["public_id"])

        db.session.add(project)
        db.session.commit()

        project_resp = get_project_data(self, data["public_id"])
        project_data = json.loads(project_resp.data.decode())

        self.assertTrue(project_resp.status)
        self.assertEquals(project_resp.status_code, 200)
        self.assertEquals(project_data["project"]["content"], data["content"])

        # Test a 404 request
        project_404_resp = get_project_data(self, 69)
        self.assertEquals(project_404_resp.status_code, 404)