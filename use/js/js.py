def main(use, **kwargs):
    """."""
    from anvil.js import import_from, new
    from anvil.js.window import Blob, Object, Reflect, URL, window

    _ = {}

    class js:

        def __getattr__(self, key: str):
            return self[key]

        def __getitem__(self, key: str):
            item = getattr(window, key, None)
            return item

        def freeze(self, target):
            """Freezes target (shallowly)."""
            return Object.freeze(target)

        def module(self, text: str, path: str = None):
            """Returns constructed JS module (no caching)."""
            if path:
                text = f"{text}\n//# sourceURL={path}"
            blob = new(Blob, [text], dict(type="text/javascript"))
            url = URL.createObjectURL(blob)
            result = import_from(url)
            URL.revokeObjectURL(url)
            return result

        def new(self, target):
            def create(*args, **kwargs):
                if kwargs:
                    args = [*args, kwargs]
                return new(target, *args)

            return create

        def object(self, **kwargs):
            """Returns JS vanilla object."""
            result = Object.create({})
            for key, value in kwargs.items():
                result[key] = value
            return result

        def pop(self, target, key: str, default=None):
            """Deletes and returns value from object by key."""
            # HACK Circumvents Anvil-Python's lack of support for JS 'delete'.
            if key in target:
                value = target[key]
                Reflect.deleteProperty(target, key)
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
                type_name = Object.prototype.toString.call(value)[8:-1]
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

    js = js()

    return js
