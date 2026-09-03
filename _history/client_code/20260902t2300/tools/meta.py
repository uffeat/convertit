from anvil import app
from anvil.server import get_app_origin
from .base import Base


class Meta(Base):
    def __init__(self):
        Base.__init__(self)
        env = app.environment.name
        self._.update(
            DEV=(env == "development"),
            PROD=(env == "production"),
            env=env,
            name=app.package_name,
        )

    @property
    def origin(self) -> str:
        origin = self._.get("origin")
        if not origin:
            origin = get_app_origin()
            self._["origin"] = origin
        return origin


meta = Meta()

export = meta
