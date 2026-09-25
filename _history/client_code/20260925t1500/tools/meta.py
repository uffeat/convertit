from anvil import app, is_server_side

from .base import Base

if is_server_side():
    from anvil.server import get_app_origin

    origin = get_app_origin()

else:
    from anvil import app_path as origin


class meta(Base):
    def __init__(self):
        Base.__init__(self)
        env = app.environment.name

        self._.update(
            DEV=(env == "development"),
            PROD=(env == "production"),
            env=env,
            name=app.package_name,
            ##origin=get_app_origin(),
            origin=origin,
        )

    def side(self, side: str = None):
        _side = "server" if is_server_side() else "client"
        if side:
            return _side == side
        return _side


meta = meta()
