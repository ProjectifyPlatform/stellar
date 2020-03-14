import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.user import User

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user, profile


def get_user_data(self, access_token, username):
    return self.client.get(
        f"/api/user/get/{username}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def update_user(self, access_token, data):
    return self.client.put(
        "/api/user/update",
        data=json.dumps(data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


class TestUserBlueprint(BaseTestCase):
    def test_user_get(self):
        """ Test getting a user from DB """

        # Create a mock user
        username = profile["username"]
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(user.id)

        user_resp = get_user_data(self, access_token, username)
        user_data = json.loads(user_resp.data.decode())

        self.assertTrue(user_resp.status)
        self.assertEquals(user_resp.status_code, 200)
        self.assertEquals(user_data["user"]["username"], username)

        # Test a 404 request
        user_404_resp = get_user_data(self, access_token, "non.existent")
        self.assertEquals(user_404_resp.status_code, 404)

    def test_user_update(self):
        """ Test updating user record """

        # Create user
        orig_data = dict(username=profile["username"], bio=profile["job"],)
        user = User(username=orig_data["username"], bio=orig_data["bio"])

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(user.id)

        # Update
        updated_data = dict(username="gen.too", bio="linux",)
        update_resp = update_user(self, access_token, updated_data)

        # Compare changes
        updated_user = User.query.get(user.id)

        self.assertTrue(update_resp)
        self.assertEqual(update_resp.status_code, 200)

        self.assertNotEqual(updated_user.username, orig_data["username"])
        self.assertNotEqual(updated_user.bio, orig_data["bio"])
