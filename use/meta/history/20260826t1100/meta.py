def main(use, Base=None, anvil=None, **kwargs):
    """."""

    class Meta(Base):
        def __init__(self):
            Base.__init__(self)
            env = anvil.app.environment.name
            self._.update(
                DEV=(env == "development"),
                PROD=(env == "production"),
                env=env,
                name=anvil.app.package_name,
            )

        @property
        def origin(self) -> str:
            origin = self._.get("origin")
            if not origin:
                origin = anvil.server.get_app_origin()
                self._["origin"] = origin
            return origin

   
    value = Meta()
    
    def load(caller):
        return value

    return load
    
