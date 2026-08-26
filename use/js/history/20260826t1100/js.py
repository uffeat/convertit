def main(use, Base=None, anvil=None, **kwargs):
    """."""

    window = anvil.window
    
    
    import_from = anvil.js.import_from
    new = anvil.js.new
    
    class Js(Base):

        def __init__(self):
            Base.__init__(self)

        def __getattr__(self, key: str):
            return self[key]

        def __getitem__(self, key: str):
            if key in self._:
                return self._[key]
            item = getattr(window, key, None)
            return item

        def freeze(self, target):
            """Freezes target (shallowly)."""
            return self.Object.freeze(target)

        def module(self, text: str, path: str = None):
            """Returns constructed JS module (no caching)."""
            if path:
                text = f"{text}\n//# sourceURL={path}"
            blob = new(self.Blob, [text], dict(type="text/javascript"))
            url = self.URL.createObjectURL(blob)
            result = import_from(url)
            self.URL.revokeObjectURL(url)
            return result

        def new(self, target):
            def create(*args, **kwargs):
                if kwargs:
                    args = [*args, kwargs]
                return new(target, *args)

            return create

        def object(self, **kwargs):
            """Returns JS vanilla object."""
            result = self.Object.create({})
            for key, value in kwargs.items():
                result[key] = value
            return result

        def pop(self, target, key: str, default=None):
            """Deletes and returns value from object by key."""
            # HACK Circumvents Anvil-Python's lack of support for JS 'delete'.
            if key in target:
                value = target[key]
                self.Reflect.deleteProperty(target, key)
                return value
            else:
                return default

        def pythonize(self, value):
            """Casts nested JS structure to equivalent Python structure.
            NOTE Supported containers: Array, vanilla JS object, dict, list."""
            # Python containers
            if isinstance(value, list):
                return [self.pythonize(v) for v in value]
            if isinstance(value, dict):
                return {k: self.pythonize(v) for k, v in value.items()}
            # JS containers
            if self.type(value) == "Array":
                return [self.pythonize(item) for item in value]
            if self.type(value) == "Object":
                return {str(k): self.pythonize(value[k]) for k in value.keys()}
            # Non-container
            return value

        def type(self, value, *refs):
            """Returns type name as JS sees it - or checks against refs."""
            try:
                type_name = self.Object.prototype.toString.call(value)[8:-1]
            except:
                type_name = ""
            if refs:
                for ref in refs:
                    if ref == type_name:
                        return True
                return False
            return type_name

        def use(self, *args):
            """."""
            return import_from(*args)

    value = Js()

    def load(caller):
        return value

    return load


   
