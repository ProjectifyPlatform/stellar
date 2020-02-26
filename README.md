# Stellar

Projectify's backend written in Flask Python (3.8).
Stellar is a free and open source REST API.

# Features

* Full featured framework for fast, easy, and documented API with [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
* JSON Web Token Authentication with [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
* Swagger Documentation (Part of Flask-RESTX).
* Unit Testing.
* Database ORM with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* Database Migrations using [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
* Object serialization/deserialization with [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* Data validations with Marshmallow [Marshmallow](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation)

# Pre-requisites

This boilerplate uses `SQLite` as its database, make sure you have it installed.
`Pipenv` is recommended to help manage the dependencies and virtualenv.

You can also use other DBs like `PostGreSQL`, make sure you have it setup and update your `DATABASE_URL` in your configs.
Read more at [Flask-SQLAlchemy's](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) documentations.

It uses [Black](https://github.com/psf/black) for code styling/formatting.

# Usage

## Installing
```sh
# Clone the repo
$ git clone https://github.com/X1Zeth2X/flask-restx-boilerplate.git

# Install packages with pipenv
$ pipenv install
```

## Running
Please specify your app's environment variables in a `.env` file, otherwise Flask CLI wouldn't find your app.

```sh
# .env file example
export FLASK_APP=stellar
export FLASK_ENV=development

# configs: production, testing, development, and default (uses DevelopmentConfig)
export FLASK_CONFIG=development

# Another way of assigning environment variables is:
FLASK_APP=stellar
FLASK_CONFIG=development

# Read more at https://github.com/theskumar/python-dotenv
```

```sh
# Enter the virtualenv
$ pipenv shell

# Run the app
$ flask run
```

## Unit testing
Stellar has already some unit tests written, we encourage adding more unit tests as you scale.

```sh
# Unit testing
$ flask test

# Run specific unit test(s)
$ flask test tests.test_auth_api tests.test_user_model ...
```
