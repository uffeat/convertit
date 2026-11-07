import pathlib


class Path:
    def __init__(self, *args, **kwargs):

        path = next((a for a in args if isinstance(a, str)), "")
        _path = pathlib.Path.cwd() / path
        parts = tuple(_path.parts[3:])

        self._.update(
            path=path,
            parts=parts,
            type=_path.suffix[1:],
            types=".".join([t[1:] for t in _path.suffixes]),
        )

        if len(parts) > 1:
            self._.update(
                parent=parts[-2],
                source=parts[0],
            )

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


class Hooks:
    def __init__(self, *args, **kwargs):
        """."""

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def keys(self, *args, **kwargs):
        return self._.keys()

    def get(self, *args, **kwargs) -> dict:
        """."""
        key = next((a for a in args), None)
        return self._.get(key, {})

    def hook(self, *args, **kwargs):
        """Decorates hook."""
        key = next((a for a in args if isinstance(a, str)), None)
        keys = [a for a in args if a is not key and isinstance(a, str)]

        def register(target: type):
            hook = target(*args, **kwargs) if hasattr(target, "__init__") else target()
            self._.setdefault(key, {}).update({a: hook for a in keys})
            return target

        return register


class use:

    def __init__(self, *args, **kwargs):
        self._.update(_cache={}, hooks=Hooks())

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
                parcel = dict(_={})
                path = Path(specifier)

                for k in self.hooks.keys():

                    hook = self.hooks.get(k).get(path[k])

                    if callable(hook):
                        updates = hook(path, **parcel)
                        if isinstance(updates, dict):
                            parcel.update(updates)

            # Get key
            options = {"key": k for k, v in kwargs.items() if k in parcel and v is True}
            key = options.get("key", parcel.get("default", "text"))

            # Get result
            result = parcel.get(key)

            return result

    def hook(self, *args, **kwargs):
        return self.hooks.hook(*args, **kwargs)


use = use()


@use.hook("source", "_scratch", "test")
class Source:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""
        path = next((a for a in args if isinstance(a, Path)), None)
        if path:
            text = (pathlib.Path.cwd() / path.path).read_text(encoding="utf-8").strip()
            return dict(text=text)
        return {}


@use.hook("type", "py")
class Py:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""
        path = next((a for a in args if isinstance(a, Path)), None)
        text = kwargs.get("text")
        if text:
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main", None)
            if callable(main):
                value = main(self, locals=locals, path=path)
                if value is not None:
                    return dict(value=value, default="value")
        return {}


if __name__ == "__main__":

    foo = use("test/foo.foo.py")
    print("foo:", foo)
