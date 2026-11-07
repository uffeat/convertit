import pathlib


class Path:
    def __init__(self, *args, **kwargs):

        specifier = next(iter(args), None)
        if isinstance(specifier, str):
            _path = pathlib.Path.cwd() / specifier
            parts = tuple(_path.parts[3:])
            self._.update(
                path=specifier,
                parts=parts,
                type=_path.suffix[1:],
                types=".".join([t[1:] for t in _path.suffixes]),
            )
            if len(parts) > 1:
                self._.update(
                    parent=parts[-2],
                    source=parts[0],
                )
        elif isinstance(specifier, self.__class__):
            self._.update(dict(specifier))
        elif isinstance(specifier, dict):
            self._.update(dict(specifier))

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        return self._.get(key)

    def __str__(self):
        return self._.get("path", "")

    def keys(self, *args, **kwargs):
        return self._.keys()


class Hooks:
    def __init__(self, *args, **kwargs):
        """."""

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __call__(self, *args, **kwargs):
        """Decorates hook."""
        # Convert args
        args = {i: v for i, v in enumerate(args)}
        # Update kwargs from args
        kwargs.update(
            {
                "_": args.pop(i)
                for i, v in [(i, cast(v)) for i, v in args.items()]
                if v is not None
            }.get("_", {})
        )
        # Re-convert args
        args = tuple(args.values())
        # Get registration keys
        if kwargs:
            key, values = next(iter(kwargs.items()), None)
            if isinstance(values, str):
                values = [values]

            def register(target: type):
                hook = (
                    target(*args, **kwargs) if hasattr(target, "__init__") else target()
                )
                container = [hook,[args, kwargs]]
                self._.setdefault(key, {}).update({a: container for a in values})
                return target

            return register

    def __getitem__(self, key) -> dict:
        return self._.get(key, {})

    def __iter__(self) -> iter:
        return iter(self._)


def cast(*args, **kwargs):
    """."""
    _ = iter(args)
    value, type = next(_, None), next(_, dict)

    try:
        return type(value)
    except:
        return


class use:

    def __init__(self, *args, **kwargs):
        self._.update(_cache={}, hooks=Hooks(), processors=Hooks())

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
        # Convert args
        args = {i: v for i, v in enumerate(args)}
        # Extract specifier
        specifier = {
            "_": args.pop(i) for i, v in [*args.items()] if isinstance(v, str)
        }.get("_")
        # Update kwargs from args
        kwargs.update(
            {
                "_": args.pop(i)
                for i, v in [(i, cast(v)) for i, v in args.items()]
                if v is not None
            }.get("_", {})
        )

        # Re-convert args
        args = tuple(args.values())

        print("specifier:", specifier)##



        if specifier:
            # Parse specifier
            path = Path(specifier)
            # Get parcel
            if specifier in self._cache:
                parcel = self._cache[specifier]
            else:
                parcel = dict(_={})

                for k in self.hooks:
                    container = self.hooks[k].get(path[k])
                    if isinstance(container, (tuple, list)):
                        hook, detail = container
                    else:
                        hook, detail = container, None
                    if callable(hook):
                        updates = hook(path, **parcel)
                        if isinstance(updates, dict):
                            parcel.update(updates)

                if parcel.get("cache", True):
                    self._cache[specifier] = parcel

            # Get key

            key = {
                "key": k for k, v in kwargs.items() if k in parcel and v is True
            }.get("key", parcel.get("default", "text"))

            # Get result
            result = parcel.get(key)

            if parcel.get("process", True):
                for k in self.processors:
                    container = self.processors[k].get(path[k])
                    if isinstance(container, (tuple, list)):
                        processor, detail = container
                    else:
                        processor, detail = container, None


                    if callable(processor):
                        _result = processor(path, result, *args, **kwargs)
                        if _result is not None:
                            result = _result

            return result

    def hook(self, *args, **kwargs):
        return self.hooks(*args, **kwargs)

    def processor(self, *args, **kwargs):
        return self.processors(*args, **kwargs)


use = use()


@use.hook(source=["_scratch", "test"])
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


@use.hook(type=["py"])
class Py:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""
        path = next((a for a in args if isinstance(a, Path)), None)
        text = kwargs.get("text")
        if isinstance(text, str):
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main", None)
            if callable(main):
                kwargs.update(locals=locals, path=path)
                value = main(use, **kwargs)
                if value is not None:
                    return dict(value=value, default="value")
        return {}


@use.hook(dict(type="json"))
class cls:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""
        from json import loads

        def load():
            return loads(kwargs.get("text"))

        value = loads(kwargs.get("text"))

        return dict(value=value, default="value", cache=False)


@use.processor(types=["foo.py"])
class cls:
    """."""

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, *args, **kwargs):
        """."""
        path, result, *args = args

        print("result:", result)

        def result():
            return args, kwargs

        return result


if __name__ == "__main__":

    print("hooks:", use.hooks._)





    Bar = use("test/foo/bar.py")
    print("Bar:", Bar)

    foo = use("test/foo.foo.py")
    foo = use("test/foo.foo.py", foo=42)
    print("foo():", foo())

    foo_json = use("test/foo/foo.json", text=True)
    print("foo_json:", foo_json)

    foo_json = use("test/foo/foo.json", dict(text=True))
    print("foo_json:", foo_json)

    foo = use("test/foo/foo.json")
    foo["name"] = "changed.."
    print("foo:", foo)

    foo = use("test/foo/foo.json")
    print("foo:", foo)
