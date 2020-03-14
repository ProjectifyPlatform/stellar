import json
from flask_jwt_extended import create_access_token

from app import db
from app.models.content import Project

from tests.utils.base import BaseTestCase


def get_project_data(self, public_id):
    return self.client.get(
        f"/api/project/{public_id}", content_type="application/json",
    )


def create_project(self, access_token, data):
    return self.client.post(
        "/api/project/create",
        data=json.dumps(data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def delete_project(self, access_token, public_id):
    return self.client.delete(
        f"/api/project/{public_id}",
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
        self.assertEqual(project_resp.status_code, 200)
        self.assertEqual(project_data["project"]["content"], data["content"])

        # Test a 404 request
        project_404_resp = get_project_data(self, 69)
        self.assertEqual(project_404_resp.status_code, 404)

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
            category_id=1,
        )

        from app.models.user import User, Role

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

        # Remove category id
        data.pop("category_id")

        # Check if each field matches.
        for field in data:
            self.assertEqual(project[field], data[field])

        # Test for bad request
        data.pop("title")
        bad_create_resp = create_project(self, access_token, data)

        self.assertEqual(bad_create_resp.status_code, 400)

    def test_project_delete(self):
        """ Test Project deletion """
        # Create a mock user & project
        from app.models.user import User

        u = User(email="test@user.com", password="gentoo")

        db.session.add(u)
        db.session.commit()

        p = Project(creator_id=u.id, public_id=123)

        db.session.add(p)
        db.session.commit()

        access_token = create_access_token(identity=u.id)

        delete_resp = delete_project(self, access_token, p.public_id)
        self.assertTrue(delete_resp.status)
        self.assertEqual(delete_resp.status_code, 200)

        # Check if project is gone ;(
        query_project = Project.query.filter_by(public_id=p.public_id).first()
        self.assertIsNone(query_project)
