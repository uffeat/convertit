class AttributeMixin:
    def __call__(self, *args):
        """Dynamic combined getter/setter."""
        # NOTE Useful in JS, which does not understand Python's object model.
        if not args:
            return self
        if len(args) == 1:
            first = args[0]
            if hasattr(first, "keys") and callable(first.keys):
                # Object-like first arg => batch setter
                for key in first.keys():
                    value = first[key]
                    setattr(self, key, value)
                return self
            # Non-object-like first arg => classic getter
            return getattr(self, first, None)
        # More than 1 arg -> classic setter
        key, value, *_ = args
        setattr(self, key, value)
        return self
