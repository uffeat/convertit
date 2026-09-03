# XXX TODO Import from client_code/tools

from anvil import app, is_server_side
from anvil.server import get_app_origin


class meta:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    @property
    def DEV(self) -> bool:

        return self.env == "development"

    @property
    def PROD(self) -> bool:
        return self.env == "production"

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

