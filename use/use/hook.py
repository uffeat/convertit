def main(use: callable, **kwargs) -> type:
    """."""
   
    
    class Hook:

        def __init__(self, owner=None):
            self.__dict__.update(__={})
            self._.update(cache={}, owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        @property
        def cache(self):
            return self._["cache"]

        @property
        def owner(self):
            return self._["owner"]
        
    return Hook
