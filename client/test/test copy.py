def main(
    Base: type = None,
    log: callable = None,
    **kwargs,
):
    """."""

    # XXX prelim use
    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            path = specifier[len("use") :]
            if path in self._cache:
                return self._cache[path]

            if self.meta.DEV:
                try:
                    text = self.anvil.server.call(f"_use", path)
                except:
                    text = self._get_text(path)
            else:
                text = self._get_text(path)

            if path.endswith(".py"):
                locals = {}
                exec(text, {}, locals)
                main = locals.pop("main", None)
                result = main(
                    self,
                    path=specifier,
                    log=self.Log(path=specifier),
                    text=text,
                    **locals,
                )
            elif path.endswith(".js"):
                ...
            else:
                return

            self._cache[path] = result
            return result

        def _get_text(self, path) -> str:
            """Returns uncached text from sheet."""
            node = self.document.createElement("div")
            node.setAttribute("__path__", path)
            self.document.head.append(node)
            value = (
                self.js.getComputedStyle(node).getPropertyValue(f"--__use__").strip()
            )
            node.remove()
            text = self.js.atob(value[1:-1])
            return text

    use = Use(Base=Base, **kwargs)

    ##log('ping:', use('use/ping.py'))##

    class Uid(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _value=0, **kwargs)

        def __call__(self) -> int:
            result = self._value
            self._value += 1
            return result

    class Registry(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _registry={}, **kwargs)

        def __call__(self, *keys, **kwargs):
            """Registers callable."""
            if keys:
                if callable(keys[-1]):
                    keys = list(keys)
                    value = keys.pop()
                    keys = tuple(keys)
                else:
                    value = None
            else:
                value = None

            # NOTE Reliable alternative to using 'global'
            context = dict(keys=keys)

            def register(value):
                keys = context["keys"]
                if not keys:
                    keys = tuple([value.__name__])
                # NOTE Create 'stored' once - NOT in keys loop!
                stored = dict(keys=keys, value=value, kwargs=kwargs)
                for key in keys:
                    self._registry[key] = stored
                return value

            if not value:
                return register
            return register(value)

        def __contains__(self, key) -> bool:
            return key in self._registry

        def __getitem__(self, key):
            """Returns instance."""
            if key in self:
                stored: dict = self._registry[key]
                value = stored["value"]
                if isinstance(value, type):
                    ##print("Instantiating for:", key)  ##
                    kwargs = stored.get("kwargs")
                    if "__init__" in value.__dict__:
                        value = value(owner=self, **kwargs)
                    else:
                        value = value()
                    stored.update(value=value)
                return value

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)
            # Create top-level container
            node = self.document.createElement("div")
            node.attachShadow(dict(mode="open"))
            slot = self.document.createElement("slot")
            node.shadowRoot.append(slot)
            node.id = "use"
            self.document.body.append(node)
            self._.update(
                node=node,
                processor=self.Registry(owner=self),
                _session=self.Uid(),
                source=self.Registry(owner=self),
                transpiler=self.Registry(owner=self),
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            session = self._session()
            path = self.Path(specifier)

            if path.full in self._cache:
                parcel = self._cache[path.full]
            else:
                # Create minimal parcel
                parcel = dict()
                if path.source in self.source:
                    updates = self.source[path.source](path=path)
                    if updates:
                        parcel.update(**updates)

                self._cache[path.full] = parcel

            # Enable kwargs from JS
            kwargs.update(
                **next(iter([a for a in args if self.js.type(a, "Object")]), {})
            )

            key = kwargs.get("key", parcel.get("default"))

            if key in parcel:
                result = parcel[key]
            else:
                if path.type in self.transpiler:
                    updates = self.transpiler[path.type](path=path, **parcel)
                    if updates:
                        parcel.update(**updates)
                else:
                    parcel.update(default="text")
                if not key:
                    key = parcel.get("default")
                result = parcel.get(key)

            if key == "load":
                result = result(caller=kwargs.get("caller"), session=session)

            if path.types in self.processor:
                process = self.processor[path.types]
                processed = process(result, *args, **kwargs)
                if processed is not None:
                    result = processed

            return result

    use = Use(Base=Base, Registry=Registry, Uid=Uid, **kwargs)

    @use.source("use")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(
            self,
            path=None,
        ) -> dict:
            node = use.document.createElement("div")
            node.setAttribute("__path__", path.path)
            use.node.append(node)
            message = {}
            if use.meta.DEV:
                try:
                    text = use.anvil.server.call(f"_use", path.full)
                    message.update(test=True)
                except use.anvil.server.UplinkDisconnectedError as error:
                    text = self._get_text(node=node, path=path)
                except Exception as error:
                    raise ValueError(f"Invalid path: {path.full}. Error: {str(error)}")
            else:
                text = self._get_text(node=node, path=path)

            if use.meta.DEV:
                child = use.document.createElement("pre")
                child.textContent = text
                child.style.display = "none"
                node.append(child)

            return dict(node=node, text=text, **message)

        def _get_text(self, node=None, path=None) -> str:
            """Returns uncached text from sheet."""
            value = (
                use.js.getComputedStyle(node)
                .getPropertyValue(f"--__{self.key}__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid path: {path.full}.")
            text = use.js.atob(value[1:-1])
            return text

    @use.transpiler("css")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, node=None, path=None, test=False, text=None, **kwargs):
            """Returns transpiled value."""
            Future = use("use/future/future.py")
            link = use.document.createElement("link")
            link.rel = "stylesheet"
            link.setAttribute("path", path.path)

            ##href = f"{path.path}?content={use.js.btoa(text)}&encoding=base64"
            href = f"{path.path}?content={text}"
            link.href = href
            future = Future()

            def load(event):
                future()

            link.addEventListener("load", load, dict(once=True))

            use.document.head.append(link)

            future.wait()

            return link

    @use.transpiler("js")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, node=None, path=None, test=False, text=None, **kwargs):
            """Returns transpiled value."""
            module = use.js.module(text, path=path.path)
            if hasattr(module, "default"):
                main = module.default
                value = main(
                    use,
                    dict(
                        node=node,
                        path=path.full,
                        test=test,
                    ),
                )
                if use.js.type(value, "Array", "Object"):
                    value = use.js.freeze(value)
                return value
            return module

    @use.transpiler("py")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, path=None, text=None, **kwargs) -> dict:

            locals = {}
            exec(text, {}, locals)
            main = locals.pop("main", None)
            if main:
                kwargs.update(locals)

                def _use(*args, **kwargs):
                    return use(*args, caller=path, **kwargs)

                value = main(
                    _use,
                    Base=use.Base,
                    anvil=use.anvil,
                    document=use.document,
                    js=use.js,
                    meta=use.meta,
                    window=use.window,
                    log=use.Log(path=path.full),
                    path=path,
                    text=text,
                    **kwargs,
                )

                ##log("type_name:", type(value).__name__)  ##

                if callable(value) and value.__name__ == "load":

                    def load(*args, **kwargs):
                        result = value(*args, **kwargs)
                        if isinstance(result, dict):
                            result = use.js.freeze(result)
                        return result

                    return dict(default="load", load=load)

                if isinstance(value, dict):
                    return dict(default="value", value=use.js.freeze(value))

                return dict(default="value", value=value)

            return dict(default="value", value=use.js.freeze(locals))

    @use.processor("json")
    class cls(use.Base):
        def __init__(self, **kwargs):
            from json import loads

            use.Base.__init__(self, _parse=loads, **kwargs)

        def __call__(self, result, *args, **kwargs):
            """."""
            if kwargs.get("key") != "text":
                return self._parse(result)

    # Set up test harness
    if use.meta.DEV:

        def test(path: str) -> None:
            """Runs test script."""
            text = use.anvil.server.call(f"_test", path)
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            main(
                use,
                log=use.Log(path=path),
                path=path,
                test=True,
            )

        @use.window.on()
        def keydown(event):
            if event.code == "KeyU" and event.shiftKey:
                stored = use.js.localStorage.getItem("__test__")
                path = use.window.prompt("Path:", stored)
                if path:
                    use.js.localStorage.setItem("__test__", path)
                    test(path)

    def _():

        Foo, foo = use("use/foo/foo.py")
        log("foo:", foo())
        ##log("text:", use("use/foo/foo.py", key="text"))
        log("html:", use("use/foo/foo.html"))

        foo = use("use/foo/foo.json")
        foo["foo"] = 43
        log("json:", foo)
        log("json:", use("use/foo/foo.json"))
        log("json:", use("use/foo/foo.json", key="text"))

        ##use("use/foo/bar/bar.py").bar()
        ##log("node:", use("use/foo/bar/bar.py").node)

    _()

    log("ping:", use("use/ping.py")())  ##
    log("ping:", use("use/ping.py")())  ##

    log("pong:", use("use/pong.py").pong())  ##
