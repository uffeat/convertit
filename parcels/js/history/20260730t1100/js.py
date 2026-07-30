def main(use, **kwargs):
    """."""
    from anvil.js import new
    from anvil.js.window import globalThis as _js

    _ = {}

    class js:

        def __getattr__(self, key: str):
            return self[key]

        def __getitem__(self, key: str):
            item = getattr(_js, key, None)
            if callable(item):

                def create(*args, **kwargs):
                    if kwargs:
                        args = [*args, kwargs]
                    try:
                        return new(item, *args)
                    except:
                        return item(*args)

                return create

            return item

        def freeze(self, target):
            """Freezes target (shallowly)."""
            return _js.Object.freeze(target)

        def use(self, url: str):
            """."""
            use = _.get("use")
            if not use:
                use = _js.Function("url", "return import(url)")
                _["use"] = use
            return use(url)

        def isinstance(self, value, *refs) -> bool:
            """Wrapper for the JS instanceof operator."""
            instanceof = _.get("instanceof")
            if not instanceof:
                instanceof = _js.Function("value, ref", "return value instanceof ref")
                _["instanceof"] = instanceof
            for ref in refs:
                if instanceof(value, ref):
                    return True
            return False

        def module(self, text: str, path: str = None):
            """Returns constructed JS module (no caching)."""
            if path:
                text = f"{text}\n//# sourceURL={path}"

            blob = new(_js.Blob, [text], dict(type="text/javascript"))
            url = _js.URL.createObjectURL(blob)
            result = self.use(url)
            _js.URL.revokeObjectURL(url)
            return result

        def new(self, target):
            def create(*args, **kwargs):
                if kwargs:
                    args = [*args, kwargs]
                return new(target, *args)

            return create

        def object(self, **kwargs):
            """Returns JS vanilla object."""
            result = _js.Object.create({})
            for key, value in kwargs.items():
                result[key] = value
            return result

        def pop(self, target, key: str, default=None):
            """Deletes and returns value from object by key."""
            # HACK Circumvents Anvil-Python's lack of support for JS 'delete'.
            if key in target:
                value = target[key]
                _js.Reflect.deleteProperty(target, key)
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
                type_name = _js.Object.prototype.toString.call(value)[8:-1]
            except:
                type_name = ""
            if refs:
                for ref in refs:
                    if ref == type_name:
                        return True
                return False

            return type_name

    js = js()

    return js
