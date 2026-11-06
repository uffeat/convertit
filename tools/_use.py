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

    def get(self, *args, **kwargs) -> callable:
        """."""
        container = next((a for a in args if isinstance(a, str)), self._)
        key = next((a for a in args if isinstance(a, str)), None)
        if key in container:
            result = container[key]
        




        keys = {i: v for i, v in enumerate(args) if isinstance(v, str)}
        container: dict = self._.get(keys.get(0), {})
        hook = container.get(keys.get(1), None)
        return hook

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

                text = (pathlib.Path.cwd() / path.path).read_text(encoding="utf-8").strip()

                parcel.update(text=text)

                

                # .py
                locals = {}
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

    def hook(self, *args, **kwargs):
        return self.hooks.hook(*args, **kwargs)


use = use()


@use.hook("type", "py")
class Py:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""
        print("Transpiling py...")


if __name__ == "__main__":
    print("hooks:", use.hooks._)


    foo = use("test/foo.foo.py")
