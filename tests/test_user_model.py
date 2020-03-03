from app.models.user import User, Role, Permission
from app.models.schemas import UserSchema

from tests.utils.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def setUp(self):
        # Extend setUp
        super(TestUserModel, self).setUp()
        Role.insert_roles()

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="penguin")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_salts_are_random(self):
        u = User(password="penguin")
        u2 = User(password="penguin")
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_role(self):
        u = User(email="test@user.com", password="gentoo")
        r = Role.query.all()

        self.assertTrue(u.has_role(Permission.FOLLOW))
        self.assertTrue(u.has_role(Permission.COMMENT))
        self.assertTrue(u.has_role(Permission.WRITE))
        self.assertFalse(u.has_role(Permission.MODERATE))
        self.assertFalse(u.has_role(Permission.CREATE))
        self.assertFalse(u.has_role(Permission.ADMIN))

    def test_creator_role(self):
        r = Role.query.filter_by(name="Creator").first()
        u = User(email="test@user.com", password="gentoo", role=r)

        self.assertTrue(u.has_role(Permission.FOLLOW))
        self.assertTrue(u.has_role(Permission.COMMENT))
        self.assertTrue(u.has_role(Permission.WRITE))
        self.assertTrue(u.has_role(Permission.CREATE))
        self.assertFalse(u.has_role(Permission.MODERATE))
        self.assertFalse(u.has_role(Permission.ADMIN))

    def test_moderator_role(self):
        r = Role.query.filter_by(name="Moderator").first()
        u = User(email="john@example.com", password="cat", role=r)

        self.assertTrue(u.has_role(Permission.FOLLOW))
        self.assertTrue(u.has_role(Permission.COMMENT))
        self.assertTrue(u.has_role(Permission.WRITE))
        self.assertTrue(u.has_role(Permission.CREATE))
        self.assertTrue(u.has_role(Permission.MODERATE))
        self.assertFalse(u.has_role(Permission.ADMIN))

    def test_administrator_role(self):
        r = Role.query.filter_by(name="Admin").first()
        u = User(email="test@user.com", password="gentoo", role=r)

        self.assertTrue(u.has_role(Permission.FOLLOW))
        self.assertTrue(u.has_role(Permission.COMMENT))
        self.assertTrue(u.has_role(Permission.WRITE))
        self.assertTrue(u.has_role(Permission.CREATE))
        self.assertTrue(u.has_role(Permission.MODERATE))
        self.assertTrue(u.has_role(Permission.ADMIN))

    def test_schema(self):
        u = User(username="gentoo", password="penguin")
        u_dump = UserSchema().dump(u)

        self.assertTrue(u_dump["username"] == "gentoo")

        with self.assertRaises(KeyError):
            u_dump["password_hash"]
