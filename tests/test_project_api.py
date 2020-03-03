import json

from app import db
from app.models.content import Project

from tests.utils.base import BaseTestCase


def get_project_data(self, public_id):
    return self.client.get(
        f"/api/project/get/{public_id}", content_type="application/json",
    )


def create_project(self, access_token, data):
    return self.client.post(
        f"/api/project/create",
        data=json.dumps(data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


class TestProjectBlueprint(BaseTestCase):
    def test_project_get(self):
        """ Test getting a project from DB """
        data = dict(content="Brogramming", public_id=123)
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

    def test_project_create(self):
        """ Test project creation """
        data = dict(
            title="An Experiment",
            difficulty=1,
            time_required="5 minutes",
            abstract="Create an experiment in 5 mins.",
            objective="The objective is to create something.",
            safety="No safety hazards",
            content="Start with the project, finish in 5 mins.",
        )

        from app.models.user import User, Role
        from flask_jwt_extended import create_access_token

        # Create a mock user
        Role.insert_roles()
        creator = Role.query.filter_by(name="Creator").first()
        user = User(username="test.user", role=creator)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        create_resp = create_project(self, access_token, data)
        create_resp_data = json.loads(create_resp.data.decode())

        project = create_resp_data["project"]
        self.assertTrue(create_resp.status)
        self.assertEqual(create_resp.status_code, 201)

        # Check if each field matches.
        for field in data:
            self.assertEqual(project[field], data[field])
