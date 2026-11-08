def cast(*args, **kwargs):
    """."""
    _ = iter(args)
    value, type = next(_, None), next(_, dict)

    try:
        return type(value)
    except:
        pass


class Base:

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __contains__(self, key: str) -> bool:
        return key in self._

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        # Facilitate **-unpacking
        return self._.get(key)

    def __iter__(self):
        return iter(self._)

    def __repr__(self) -> str:
        return str(self._)

    def get(self, *args, **kwargs):
        _ = iter(args)
        key, default = next(_, None), next(_, None)
        return self._.get(key, default)

    def keys(self, *args, **kwargs):
        # Facilitate **-unpacking
        return self._.keys()


class View(Base):
    def __init__(self, *args, **kwargs):
        [self._.update(a) for a in [cast(a) for a in args] if a]
        self._.update(kwargs)


class Path(Base):

    def __init__(self, *args, **kwargs):
        import pathlib

        specifier = next(iter(args), None)
        if isinstance(specifier, str):
            _ = pathlib.Path.cwd() / specifier
            parts = tuple(_.parts[3:])
            self._.update(
                name=_.name,
                path=specifier,
                parts=parts,
                stem=_.stem,
                type=_.suffix[1:],
                types=".".join([t[1:] for t in _.suffixes]),
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

    def __str__(self):
        return self._.get("path", "")


class Hooks(Base):

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
            key, values = next(iter(kwargs.items()))
            if isinstance(values, str):
                values = [values]

            def register(target: type):
                hook = (
                    target(*args, **kwargs)
                    if "__init__" in target.__dict__
                    else target()
                )
                container = dict(value=hook)
                self._.setdefault(key, {}).update({v: container for v in values})
                return target

            return register


class use(Base):

    def __init__(self, *args, **kwargs):
        self._.update(_cache={}, hooks=Hooks(), processors=Hooks())

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

        if specifier:
            # Parse specifier
            path = Path(specifier)
            # Get parcel
            if specifier in self._cache:
                parcel = self._cache[specifier]
            else:
                parcel = dict(_={})
                for k in self.hooks:
                    container: dict = self.hooks.get(k, {}).get(path[k], {})
                    hook = container.get("value")
                    if callable(hook):
                        updates = hook(path, **parcel)
                        if isinstance(updates, dict):
                            parcel.update(updates)

                if parcel.get("cache", True):
                    self._cache[specifier] = parcel
            # Get key
            key = {"_": k for k, v in kwargs.items() if k in parcel and v is True}.get(
                "_", parcel.get("default", "text")
            )

            # Get result
            result = parcel.get(key)

            # Process
            if parcel.get("process", True):
                for k in self.processors:
                    container: dict = self.processors.get(k, {}).get(path[k], {})
                    hook = container.get("value")
                    if callable(hook):
                        _result = hook(path, result, *args, **kwargs)
                        if _result is not None:
                            result = _result

            return result

    def hook(self, *args, **kwargs):
        return self.hooks(*args, **kwargs)

    def processor(self, *args, **kwargs):
        return self.processors(*args, **kwargs)


use = use()


@use.hook(source=["_scratch", "test"])
class cls:

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, path: Path, **parcel):
        """."""
        import pathlib

        text = (pathlib.Path.cwd() / path.path).read_text(encoding="utf-8").strip()
        return dict(text=text)


@use.hook(type=["py"])
class cls:

    def __call__(self, path: Path, **parcel):
        """."""
        text = parcel.get("text")
        locals = {}
        exec(text, {}, locals)
        main = locals.get("main", None)
        if callable(main):
            parcel.update(locals=locals, path=path)
            value = main(use, **parcel)
            if value is not None:
                return dict(value=value, default="value")
        return {}


##@use.processor(type=["json"])
@use.processor(dict(type="json"))
class cls:
    """."""

    def __call__(self, path: Path, result: str, *args, **kwargs):
        """."""
        if "text" not in kwargs:
            from json import loads

            return loads(result)


@use.processor(type=["py"])
class cls:
    """."""

    def __call__(self, path: Path, result, *args, **kwargs):
        """."""
        if "text" not in kwargs:
            if isinstance(result, (list, tuple)):

                return View(
                    {r.__name__: r for r in result if hasattr(r, "__name__")},
                    next((r for r in result if isinstance(r, dict)), {}),
                )


if __name__ == "__main__":

    ##print("keys:", Path().keys())##

    ##print("hooks:", use.hooks)  ##

    Bar = use("test/foo/bar.py").Bar
    print("Bar:", Bar)

    bar = use("test/foo/bar.py").bar
    print("bar:", bar)

    foo = use("test/foo.foo.py")
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

    ##print("use:", use)
