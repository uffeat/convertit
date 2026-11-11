# XXX TODO module import, inject parcels,
# mini-racer
# perhaps patch, perhaps effects, perhaps tools for args parsing, perhaps uid, perhaps caller etc.

import tools

print("tools:", tools)


print(getattr(tools, "foo", None))


def run(*args, **kwargs):
    """Decorator for controlling (encapsulating) lexical scope."""
    if callable(args[0] if args else None):
        target, *args = args
        return target(*args, **kwargs)
    return lambda target: run(target, *args, **kwargs)


@run
class cast:
    """."""

    def __call__(self, *args, **kwargs):
        args = list(args)
        cls = kwargs.pop(
            "type",
            next(
                iter([args.pop(i) for i, v in enumerate(args) if isinstance(v, type)]),
                dict,
            ),
        )
        value = kwargs.pop("value", next((v for v in args if v is not cls), None))
        result = [value, True]
        if not isinstance(value, cls):
            try:
                result[0] = cls(value)
            except:
                default = kwargs.pop(
                    "default",
                    next(
                        (v for v in args[0:] if all([v is not value, v is not cls])),
                        value,
                    ),
                )
                result = [default(value) if callable(default) else default, False]
        return result

    def batch(self, *args, **kwargs):
        args = list(args)
        cls = kwargs.pop(
            "type",
            next(
                iter([args.pop(i) for i, v in enumerate(args) if isinstance(v, type)]),
                dict,
            ),
        )
        processed = [self(v, default=kwargs.get("default", v), type=cls) for v in args]
        return [v for v, s in processed if s], [v for v, s in processed if not s]




        

    def castable(self, *args, **kwargs):
        args = list(args)
        cls = kwargs.get(
            "type",
            next(
                iter([args.pop(i) for i, v in enumerate(args) if isinstance(v, type)]),
                dict,
            ),
        )
        value = kwargs.get("value", next((v for v in args if v is not cls), None))
        if isinstance(value, cls):
            return True
        try:
            cls(value)
            return True
        except:
            return False


##
converted = cast.batch(0, 1, 2, dict, 3, dict(foo=42))
print("converted:", converted)

##


class Private(dict):

    def __call__(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def __getitem__(self, key):
        return dict.get(self, key)

    def __setitem__(self, key, value):
        getattr(dict, "pop" if value is None else "__setitem__")(self, key, value)
        return self

    def pop(self, *args, **kwargs):
        return dict.pop(self, *[*args, *[None, None][len(args) :]][0:2])

    def setdefault(self, *args, **kwargs):
        key, value = [*args, *[None, True][len(args) :]][0:2]
        if value is not None:
            return dict.setdefault(self, key, value)

    def update(self, *args, **kwargs):
        for value in args:
            value, success = cast(value)
            if success:
                kwargs.update(value)
        for key, value in kwargs.items():
            getattr(dict, "pop" if value is None else "__setitem__")(self, key, value)
        return self


class Base:

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", Private())

    def __bool__(self) -> bool:
        return bool(self._)

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

    def __len__(self) -> int:
        return len(self._)

    def __repr__(self) -> str:
        return str(self._)

    def get(self, *args, **kwargs):
        return self._.get(*[*args, *[None, None][len(args) :]][0:2])

    def items(self, *args, **kwargs):
        return self._.items()

    def keys(self, *args, **kwargs):
        # Facilitate **-unpacking
        return self._.keys()

    def values(self, *args, **kwargs):
        return self._.values()


class View(Base):
    def __init__(self, *args, **kwargs):
        for value in args:
            value, success = cast(value)
            if success:
                kwargs.update(value)
        self._(kwargs)



class Arguments(Base):
    def __init__(self, *args, **kwargs):
        """Updates kwargs from args."""
        converted = cast.batch(*args)
        [kwargs.update(u) for u in converted[0]]
        self._(
            args=converted[1],
            kwargs=Private(kwargs),
        )
        

    # XXX TODO Refactor
    def __call__(self, *args, **kwargs):
        """."""
        if args:
            predicates = [v for v in args if callable(v)]

            if predicates:
                default = next((v for v in args if v not in predicates), None)

                return next(
                    (
                        v
                        for i, v in enumerate(self.args)
                        if all([p(i, v) for p in predicates])
                    ),
                    default,
                )

        return tuple(self.values())


##
arguments = Arguments(42, {"foo": 42}, bar=8)
print("arguments.args:", arguments.args)
print("arguments.kwargs:", arguments.kwargs)
##


class PathType(Base):

    @classmethod
    def properties(cls, *args, **kwargs):
        return View(
            {
                k: v
                for k, v in cls.__dict__.items()
                if isinstance(k, str)
                and not k.startswith("_")
                and isinstance(v, property)
            }
        )

    def __init__(self, *args, **kwargs):
        import pathlib

        specifier = next(iter(args), None)
        if isinstance(specifier, str):
            _ = pathlib.Path.cwd() / specifier
            parts = tuple(_.parts[3:])
            self._(
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
            self._(dict(specifier))
        else:
            self._(specifier)

    def __str__(self):
        return self._.get("path", "")

    @property
    def source(self):
        return self._["source"]

    @property
    def type(self):
        return self._["type"]

    @property
    def types(self):
        return self._["types"]


@run
def Path() -> PathType:
    """Creates class-level state."""

    class Path(PathType):
        """Thin sub-class to preserve type-hinting."""

        @classmethod
        def properties(cls, *args, **kwargs):
            return _["properties"]

        def __init__(self, *args, **kwargs):
            PathType.__init__(self, *args, **kwargs)

    _ = dict(properties=PathType.properties())

    return Path


class Hooks(Base):

    def __call__(self, *args, **kwargs):
        """Decorates hook."""

        args, kwargs = Arguments(*args, **kwargs)()

        # Get registration keys
        registration = {
            k: kwargs.pop(k) for k, v in list(kwargs.items()) if k in Path.properties()
        }
        if registration:
            key, values = next(iter(registration.items()))
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
        self._(_cache={}, hooks=Hooks(), processors=Hooks())

    def __call__(self, *args, **kwargs):
        arguments = Arguments(*args, **kwargs)

        specifier = arguments(lambda i, v: isinstance(v, str))

        # specifier -> parcel -> result
        if specifier:
            # Parse specifier
            path = Path(specifier)
            # Get parcel
            if specifier in self._cache:
                parcel = self._cache[specifier]
            else:
                parcel = dict(_={})

                @run
                def create():
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
            key = {
                True: k
                for k, v in arguments.kwargs.items()
                if k in parcel and v is True
            }.get(True, parcel.get("default", "text"))

            # Get result (wrap for clean access from functions)
            result = dict(value=parcel.get(key))

            @run
            def process():
                if parcel.get("process", True):
                    for k in self.processors:
                        container: dict = self.processors.get(k, {}).get(path[k], {})
                        hook = container.get("value")
                        if callable(hook):
                            _result = hook(
                                path,
                                result["value"],
                                *arguments.args,
                                **arguments.kwargs
                            )
                            if _result is not None:
                                result.update(value=_result)

            return result["value"]

    def hook(self, *args, **kwargs):
        return self.hooks(*args, **kwargs)

    def processor(self, *args, **kwargs):
        return self.processors(*args, **kwargs)


use = use()


@use.hook(source=["_scratch", "test"])
class cls:

    def __init__(self, *args, **kwargs):
        """."""

    def __call__(self, path: PathType, **parcel):
        """."""
        import pathlib

        text = (pathlib.Path.cwd() / path.path).read_text(encoding="utf-8").strip()
        return dict(text=text)


@use.hook(type=["py"])
class cls:

    def __call__(self, path: PathType, **parcel):
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


@use.processor(dict(type="json"))
class cls:
    """."""

    def __call__(self, path: PathType, result: str, *args, **kwargs):
        """."""
        if "text" not in kwargs:
            from json import loads

            return loads(result)


@use.processor(type=["py"])
class cls:
    """."""

    def __call__(self, path: PathType, result, *args, **kwargs):
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
