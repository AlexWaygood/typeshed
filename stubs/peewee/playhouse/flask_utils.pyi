from _typeshed import Unused
from collections.abc import Container
from typing import Any
from typing_extensions import TypeAlias

from peewee import Database, ModelBase, Proxy

# Is actually flask.Flask
_Flask: TypeAlias = Any

class FlaskDB:
    """
    Convenience wrapper for configuring a Peewee database for use with a Flask
    application. Provides a base `Model` class and registers handlers to manage
    the database connection during the request/response cycle.

    Usage::

        from flask import Flask
        from peewee import *
        from playhouse.flask_utils import FlaskDB


        # The database can be specified using a database URL, or you can pass a
        # Peewee database instance directly:
        DATABASE = 'postgresql:///my_app'
        DATABASE = PostgresqlDatabase('my_app')

        # If we do not want connection-management on any views, we can specify
        # the view names using FLASKDB_EXCLUDED_ROUTES. The db connection will
        # not be opened/closed automatically when these views are requested:
        FLASKDB_EXCLUDED_ROUTES = ('logout',)

        app = Flask(__name__)
        app.config.from_object(__name__)

        # Now we can configure our FlaskDB:
        flask_db = FlaskDB(app)

        # Or use the "deferred initialization" pattern:
        flask_db = FlaskDB()
        flask_db.init_app(app)

        # The `flask_db` provides a base Model-class for easily binding models
        # to the configured database:
        class User(flask_db.Model):
            email = CharField()

    """

    # Omitting undocumented base_model_class on purpose, use FlaskDB.Model instead
    database: Database | Proxy
    def __init__(
        self,
        app: _Flask | None = None,
        database: Database | Proxy | None = None,
        # Is actually type[ModelClass] but stubtest likely confuses with Model property
        # https://github.com/python/typeshed/pull/11731#issuecomment-2067694259
        model_class=...,
        excluded_routes: Container[str] | None = None,
    ) -> None: ...
    def init_app(self, app: _Flask) -> None: ...
    def get_model_class(self) -> type[ModelBase]: ...
    @property
    def Model(self) -> type[ModelBase]: ...
    def connect_db(self) -> None: ...
    def close_db(self, exc: Unused) -> None: ...
