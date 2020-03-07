from datetime import datetime

from flask import current_app
from app import db, bcrypt

# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Permission:
    FOLLOW = 1
    COMMENT = 2
    # Write something about a project
    WRITE = 4
    # Create a project
    CREATE = 8

    MODERATE = 16
    ADMIN = 32


class Role(Model):
    __tablename__ = "roles"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True)
    default = Column(db.Boolean, default=False, index=True)
    permissions = Column(db.Integer)
    description = Column(db.String(50))

    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"<{self.name} - {self.id}>"

    @staticmethod
    def insert_roles():
        roles = {
            "User": [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            "Creator": [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.CREATE,
            ],
            "Moderator": [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.CREATE,
                Permission.MODERATE,
            ],
            "Admin": [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.CREATE,
                Permission.MODERATE,
                Permission.ADMIN,
            ],
        }

        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)

            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)

            role.default = role.name == default_role
            db.session.add(role)

        db.session.commit()

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0


class User(Model):
    """ User model for storing user related data """

    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15), unique=True, index=True)
    email = Column(db.String(64), unique=True, index=True)
    username = Column(db.String(15), unique=True, index=True)
    bio = Column(db.String(150))
    name = Column(db.String(64))
    password_hash = Column(db.String(128))

    # Relationships
    ## Creations
    projects = relationship("Project", backref="creator", lazy="dynamic")
    ratings = relationship("Rating", backref="rater", lazy=True)
    ## Social
    posts = relationship("Post", backref="author", lazy="dynamic")
    comments = relationship("Comment", backref="author", lazy=True)

    joined_date = Column(db.DateTime, default=datetime.utcnow)
    role_id = Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["STELLAR_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()

            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def has_role(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def __repr__(self):
        return f"<User {self.username}>"
