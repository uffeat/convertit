import json
from anvil.server import call
from ..console import console, log
from ..document import document
from ..js import js
from ..tools import Base, Path
from ..works import works
from ..window import window


class Hook(Base):

    def __init__(self, *args, use=None, **kwargs):
        Base.__init__(self)
        self._.update(cache={}, use=use)

    @property
    def use(self):
        return self._["use"]


assets = js.use("https://rolloh.vercel.app/anvil/use.js").assets
app = assets.get("@/rollo/").app

# Create use container
container = document.createElement("div")
container.setAttribute("use", "")
container.slot = "data"
app.append(container)


def create_node(path: str):
    """Creates and adds node for parcel text extraction."""
    result = document.createElement("div")
    result.setAttribute("__path__", path)
    container.append(result)
    return result


def get_text(path: str) -> str:
    """Returns (uncached) parcel text."""
    node = create_node(path)
    value = js.getComputedStyle(node).getPropertyValue("--__use__").strip()
    if not value:
        raise ValueError(f"Invalid path: {path}")
    result = js.atob(value[1:-1])
    return result


class Use(Base):
    def __init__(self):
        Base.__init__(self)
        self._.update(
            added={}, cache={}, registries=dict(source={}, transpile={}, process={})
        )

        def hook(*keys) -> callable:
            def register(cls: type, *args, **kwargs) -> type:
                key: str = getattr(cls, "hook", None)
                registries: dict = self._["registries"]
                registry: dict = registries.get(key)
                if "__init__" in cls.__dict__:
                    instance = cls(*args, use=self, **kwargs)
                else:
                    instance = cls()

                for k in keys:
                    registry[k] = instance
                return cls

            return register

        self._.update(hook=hook)

    @property
    def hook(self):
        return self._["hook"]

    def __call__(self, specifier: str, *args, **kwargs):

        ##print("use got specifier:", specifier)  ##

        # Enable invocation from JS
        kwargs.update(**next(iter(args), {}))
        # Extract options
        raw = kwargs.get("raw")
        # Get hooks registries
        registries: dict = self._["registries"]
        # Create path
        path = Path(specifier)
        # Init result
        result = None
        # Get source hook registry
        registry: dict = registries["source"]
        # Get source hook
        hook = registry.get(path.source)
        if hook:
            # Get result from source
            result = hook(path)
        if raw or path.detail.get("escape"):
            # Return result as-is
            return result
        # Transpile
        if path.detail.get("transpile", True):
            # Get transpile hook registry
            registry: dict = registries["transpile"]
            # Get transpile hook
            hook = registry.get(path.file.type)
            if hook:
                # Transpile result
                transpiled = hook(result, path, **kwargs)
                if transpiled:
                    result = transpiled
        # Process
        if path.detail.get("process", True):
            # Get process hook registry
            registry: dict = registries["process"]
            for t in path.file.types:
                hook = registry.get(t)
                if hook:
                    processed = hook(result, path, *args, **kwargs)
                    if processed:
                        result = processed

        return result

    def add(self, key, value):
        """Adds parcel."""
        added: dict = self._["added"]
        added[key] = value
        return self


use = Use()


@use.hook("/", "@")
class cls:
    hook = "source"

    def __call__(self, path: Path):
        path.detail.update(escape=True)
        return assets.get(path.specifier)


@use.hook("@@")
class cls(Base):
    hook = "source"

    def __init__(self, *args, **kwargs):
        Base.__init__(self)
        self._.update(cache={})

    def __call__(self, path: Path) -> str:
        """Returns parcel text."""
        cache = self._["cache"]
        if path.path in cache:
            result = cache[path.path]
            return result
        result = get_text(path.path)
        cache[path.path] = result
        return result


@use.hook("py")
class cls(Hook):
    hook = "transpile"

    def __init__(self, *args, **kwargs):
        Hook.__init__(self, *args, **kwargs)

    def __call__(self, text: str, path: Path, **kwargs):
        if not isinstance(text, str):
            return
        cache = self._["cache"]
        if path.path in cache:
            result = cache[path.path]
            return result

        locals = {}
        exec(text, {}, locals)
        main = locals["main"]

        annotations: dict = main.__annotations__
        print("annotations", annotations)  ##
        returns = annotations.get("return")
        print(f"{path.path} return type:", returns)  ##
        if returns is dict:
            ...
            print(f"{path.path} returns a dict")  ##

        ##print("defaults", main.__defaults__)  ##
        ##print("doc", main.__doc__)  ##
        result = main(
            use,
            anvil=works,
            console=console,
            document=document,
            js=js,
            log=log,
            main=main,
            path=path.path,
            text=text,
            window=window,
        )
        if isinstance(result, dict):
            result = js.freeze(result)

        cache[path.path] = result
        return result







@use.hook("css")
class cls(Base):
    hook = "transpile"

    def __init__(self, *args, **kwargs):
        Base.__init__(self)
        self._.update(cache={})

    def __call__(self, text: str, path: Path, **kwargs):
        if not isinstance(text, str):
            return
        link = kwargs.get("link")
        if link:
            rel = "stylesheet"
            link = document.head.querySelector(f'link[path="{path.path}"]')
            if not link:
                Future = use("@@/future/future.py")
                link = document.createElement("link")
                link.rel = rel
                link.setAttribute("path", path.path)

                href = f"{path.path}?content={text}"
                link.href = href
                future = Future()

                def load(event):
                    future()

                link.addEventListener("load", load, dict(once=True))

                document.head.append(link)

                future.wait()

            return link

        cache = self._["cache"]
        if path.path in cache:
            return cache[path.path]
        Sheet = use("@/rollo/").Sheet
        result = Sheet.create(text, path.path)
        cache[path.path] = result
        return result


@use.hook("js")
class cls(Base):
    hook = "transpile"

    def __init__(self, *args, use=None, **kwargs):
        Base.__init__(self)
        self._.update(
            cache={},
            use=use,
        )

    def __call__(self, text: str, path: Path, **kwargs):
        if not isinstance(text, str):
            return
        cache = self._["cache"]
        if path.path in cache:
            result = cache[path.path]
            return result
        module = js.module(text, path=path.path)
        main = module.default
        result = main(
            use, dict(main=main, path=path.path, text=text)
        )

        if js.type(result, "Object"):
            result = js.freeze(result)

        cache[path.path] = result
        return result


@use.hook("json")
class cls:
    hook = "transpile"

    def __call__(self, text: str, path: Path, **kwargs):
        if not isinstance(text, str):
            return
        result = json.loads(text)
        return result
