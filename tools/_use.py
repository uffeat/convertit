import pathlib


class Path(pathlib.Path):

    def __getitem__(self, key):
        return getattr(self, key, None)

    @property
    def parts(self):
        return tuple(pathlib.Path.parts.fget(self)[3:])

    @property
    def source(self):
        parts = self.parts
        return parts[0] if len(parts) > 1 else "/"

    @property
    def type(self):
        return self.suffix[1:]

    @property
    def types(self):
        return tuple([t[1:] for t in self.suffixes])


class Hooks:
    def __init__(self, *args, **kwargs):
        """."""

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __getattr__(self, key: str):
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        return self._.get(key)

    def keys(self, *args, **kwargs):
        return self._.keys()

    def set(self, *args, **kwargs):
        """."""
        value = next((a for i, a in enumerate(args) if i < 2 and callable(a)), None)
        key = next(
            (a for i, a in enumerate(args) if i < 2 and isinstance(a, str)),
            getattr(value, "__name__", value.__class__.__name__),
        )
        args = [a for a in args if a is not value and a is not key]

        if isinstance(value, type):
            value = value(*args, **kwargs) if hasattr(value, "__init__") else value()

        self._[key] = dict(value=value)

    def remove(self, *args, **kwargs):
        """."""
        key = next((a for a in args if isinstance(a, str)), '')
        self._.pop(key, None)


hooks = Hooks()


class py:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""


hooks.set(py)


print("hooks._", hooks._)  ##


class use:

    def __init__(self, *args, **kwargs):
        self._.update(_cache={})

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        # Facilitate **-unpacking
        return self._.get(key)

    def keys(self, *args, **kwargs):
        # Facilitate **-unpacking
        return self._.keys()

    def __call__(self, *args, **kwargs):
        # Parse args
        specifier = next((a for a in args if isinstance(a, str)), None)
        if specifier:
            specifier, *args = args
        # Get parcel
        if specifier in self._cache:
            parcel = self._cache[specifier]
        else:
            parcel = {}

            path = Path.cwd() / specifier

            locals = {}
            text = path.read_text(encoding="utf-8").strip()
            parcel.update(text=text)

            print("type", path.type)  ##
            print("types", path.types)  ##
            print("source", path.source)  ##
            print("parent", path.parent)  ##

            print("parts", path.parts)  ##
            print("name", path.name)  ##

            # .py
            exec(text, {}, locals)
            main = locals.pop("main", None)
            if callable(main):
                value = main(self)
                if value is not None:
                    parcel.update(value=value, default="value")

        # Get key
        options = {"key": k for k, v in kwargs.items() if k in parcel and v is True}
        key = options.get("key", parcel.get("default", "text"))

        # Get result
        result = parcel.get(key)

        return result


use = use()

if __name__ == "__main__":
    foo = use("test/foo.foo.py")
