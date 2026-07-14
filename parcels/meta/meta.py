def main(use, anvil=None, **kwargs) -> type:
    """."""

    Base = use("@@/base/base.py")
    env = anvil.anvil.app.environment.name
    get_app_origin = anvil.server.get_app_origin

    class Meta(Base):
        def __init__(self):
            Base.__init__(self)

            self._.update(
                DEV=(env == "development"),
                PROD=(env == "production"),
                env=env,
                origin=get_app_origin(),
            )

        @property
        def DEV(self) -> bool:
            return self._["DEV"]

        @property
        def PROD(self) -> bool:
            return self._["PROD"]

        @property
        def env(self) -> str:
            return self._["env"]

        @property
        def origin(self) -> str:
            return self._["origin"]

    meta = Meta()

    return meta
