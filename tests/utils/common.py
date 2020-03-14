# Commonly used test case functions.
import json
from faker import Faker


def register_user(self, data):
    return self.client.post(
        "/auth/register", data=json.dumps(data), content_type="application/json",
    )


def login_user(self, email, password):
    return self.client.post(
        "/auth/login",
        data=json.dumps(dict(email=email, password=password,)),
        content_type="application/json",
    )


# Create a fake profile.
profile = Faker().profile()
