from anvil import app, is_server_side
from anvil.server import get_app_origin
from .mixins import AttributeMixin
from ._base import Base


class meta(Base, AttributeMixin):
    def __init__(self):
        Base.__init__(self)

    @property
    def DEV(self) -> bool:
        return app.environment.name == "development"

    @property
    def PROD(self) -> bool:
        return app.environment.name == "production"

    @property
    def SERVER(self) -> bool:
        return is_server_side()

    @property
    def env(self) -> str:
        env = self._.get("env")
        if not env:
            env = app.environment.name
            self._.update(env=env)
        return env

    @property
    def origin(self) -> str:
        origin = self._.get("origin")
        if not origin:
            origin = get_app_origin()
            self._.update(origin=origin)
        return origin


meta = meta()
