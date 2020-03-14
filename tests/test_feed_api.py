import json
from faker import Faker

from app import db
from flask_jwt_extended import create_access_token

from tests.utils.base import BaseTestCase
from tests.utils.common import profile

fake = Faker()


def get_feed_posts(self, access_token, page: int):
    return self.client.get(
        f"/api/feed/posts?page={page}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def get_feed_projects(self, page: int, category: str):
    return self.client.get(f"/api/feed/projects?page={page}&category={category}")


class TestFeedBlueprint(BaseTestCase):
    def test_feed_get_posts(self):
        """ Test getting posts from feed. """
        from app.models.content import Post

        access_token = create_access_token(69)

        # Create 6 random posts
        posts = []

        for i in range(5):
            post = Post(caption=fake.text(), on_project=i)
            posts.append(post)

        db.session.bulk_save_objects(posts)
        db.session.commit()

        feed_resp = get_feed_posts(self, access_token, 1)
        feed_resp_data = json.loads(feed_resp.data.decode())

        self.assertTrue(feed_resp.status)
        self.assertEqual(feed_resp.status_code, 200)
        self.assertEqual(len(feed_resp_data["posts"]), 3)

        # Page 2
        feed_resp_2 = get_feed_posts(self, access_token, 2)
        feed_resp_2_data = json.loads(feed_resp_2.data.decode())

        self.assertTrue(feed_resp_2.status)
        self.assertEqual(feed_resp_2.status_code, 200)
        self.assertEqual(len(feed_resp_2_data["posts"]), 2)

    def test_feed_get_projects(self):
        """ Test getting projects from feed. """
        from app.models.content import Project, Category

        # Implement unit test

        # Create 2 categories
        categories = [
            Category(name="math"),
            Category(name="physics"),
        ]

        db.session.bulk_save_objects(categories)
        db.session.flush()

        # Create projects
        projects = [
            Project(content=fake.text(), category_id=1),
            Project(content=fake.text(), category_id=2),
            Project(content=fake.text(), category_id=2),
        ]

        db.session.bulk_save_objects(projects)
        db.session.commit()

        math_feed_resp = get_feed_projects(self, 1, "math")
        math_feed_resp_data = json.loads(math_feed_resp.data.decode())

        self.assertTrue(math_feed_resp.status)
        self.assertEqual(math_feed_resp.status_code, 200)
        self.assertEqual(len(math_feed_resp_data["projects"]), 1)

        physx_feed_resp = get_feed_projects(self, 1, "physics")
        physx_feed_resp_data = json.loads(physx_feed_resp.data.decode())

        self.assertTrue(physx_feed_resp.status)
        self.assertEqual(physx_feed_resp.status_code, 200)
        self.assertEqual(len(physx_feed_resp_data["projects"]), 2)
