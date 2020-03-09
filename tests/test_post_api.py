import json
from flask_jwt_extended import create_access_token

from app import db
from app.models.content import Post

from tests.utils.base import BaseTestCase


def get_post_data(self, public_id):
    return self.client.get(
        f"/api/post/get/{public_id}", content_type="application/json"
    )


def create_post(self, access_token, project_public_id, data):
    return self.client.post(
        f"/api/post/create/{project_public_id}",
        data=json.dumps(data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def update_post(self, access_token, public_id, data):
    return self.client.put(
        f"/api/post/update/{public_id}",
        data=json.dumps(data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def delete_post(self, access_token, public_id):
    return self.client.delete(
        f"/api/post/delete/{public_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
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
        # Create a mock user
        from app.models.user import User

        author = User(username="test.user")

        db.session.add(author)
        db.session.commit()

        # Create a mock project
        from app.models.content import Project

        project_public_id = 4206921
        project = Project(content="hemlo", public_id=project_public_id)

        db.session.add(project)
        db.session.commit()

        access_token = create_access_token(author.id)

        # Create post
        from hashlib import sha256

        image_hash = sha256(str("an_image").encode("utf-8")).hexdigest()[:32]
        data = dict(caption="A caption.", image_hash=image_hash)

        create_resp = create_post(self, access_token, project_public_id, data)
        create_resp_data = json.loads(create_resp.data.decode())

        post = create_resp_data["post"]

        self.assertTrue(create_resp.status)
        self.assertEqual(create_resp.status_code, 201)

        # Check if each field matches.
        for field in data:
            self.assertEqual(post[field], data[field])

        # Test for bad request
        data.pop("caption")
        bad_create_resp = create_post(self, access_token, project_public_id, data)

        self.assertEqual(bad_create_resp.status_code, 400)

    def test_post_update(self):
        """ Test post updating """
        from app.models.user import User

        u = User(email="test@user.com", password="gentoo")

        db.session.add(u)
        db.session.commit()

        orig_data = dict(caption="arch", image_hash="linux.png", public_id=4206921,)
        p = Post(
            author_id=u.id,
            caption=orig_data["caption"],
            public_id=orig_data["public_id"],
        )

        db.session.add(p)
        db.session.commit()

        access_token = create_access_token(u.id)

        # Update
        updated_data = dict(caption="gentoo")
        update_resp = update_post(
            self, access_token, orig_data["public_id"], updated_data
        )

        # Compare changes
        updated_post = Post.query.filter_by(public_id=orig_data["public_id"]).first()

        self.assertTrue(update_resp)
        self.assertEqual(update_resp.status_code, 200)

        self.assertNotEqual(updated_post.caption, orig_data["caption"])

    def test_post_deletion(self):
        """ Test post deletion """

        from app.models.user import User

        u = User(email="test@user.com", password="gentoo")

        db.session.add(u)
        db.session.commit()

        post_public_id = 4206921
        p = Post(author_id=u.id, public_id=post_public_id)

        db.session.add(p)
        db.session.commit()

        access_token = create_access_token(u.id)

        delete_resp = delete_post(self, access_token, post_public_id)
        self.assertTrue(delete_resp.status)
        self.assertEqual(delete_resp.status_code, 200)

        # Check if post is gone ;(
        query_post = Post.query.filter_by(public_id=p.public_id).first()
        self.assertIsNone(query_post)
