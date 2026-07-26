def main(use: callable, **kwargs) -> type:
    """."""
    Base = use("/base/base.py")
    
    class Hook(Base):

        def __init__(self, owner=None):
            Base.__init__(self)
            self._.update(cache={}, owner=owner)

        @property
        def cache(self):
            return self._["cache"]

        @property
        def owner(self):
            return self._["owner"]
        
    return Hook
