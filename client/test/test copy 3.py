def main(
    Base: type = None,
    anvil=None,
    log: callable = None,
    **kwargs,
):
    """."""

    class Use(Base):
        def __init__(self, **kwargs):
            DEV = (anvil.app.environment.name == "development")
            Base.__init__(self, _cache={},  DEV=DEV,**kwargs)
           

        def __call__(self, path: str, *args, **kwargs):
            """Returns result from import engine."""
            if path in self._cache:
                parcel = self._cache[path]
                
            else:
                parcel = {}

                if self.DEV:
                    try:
                        text = anvil.server.call(f"_use", path)
                    except:
                        text = self._get_text(path)
                else:
                    text = self._get_text(path)

                parcel.update(text=text)
                if path.endswith(".py"):
                    locals = {}
                    exec(text, {}, locals)
                    value =  locals["main"](self, Base=Base, anvil=anvil)
                    parcel.update(value=value) 
                elif path.endswith(".js"):
                    ...
                self._cache[path] = parcel

            result = parcel.get(kwargs.get('key', 'value'))
            return result

        def _get_text(self, path) -> str:
            """Returns uncached text from sheet."""
            node = anvil.window.document.createElement("div")
            node.setAttribute("__path__", path)
            anvil.window.document.head.append(node)
            value = (
                anvil.window.getComputedStyle(node)
                .getPropertyValue(f"--__use__")
                .strip()
            )
            node.remove()
            text = anvil.window.atob(value[1:-1])
            return text

    use = Use()

    Uid = use("use/tools/uid.py")
    Registry = use("use/use/registry.py")
    Path = use("use/path/path.py")
    document = use("use/document/document.py")
    js = use("use/js/js.py")
    meta = use("use/meta/meta.py")
    window = use("use/window/window.py")
    Log = use("use/log/log.py")

   
   

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)
            # Create top-level container
            node = document.createElement("div")
            node.attachShadow(dict(mode="open"))
            slot = document.createElement("slot")
            node.shadowRoot.append(slot)
            node.id = "use"
            document.body.append(node)
            self._.update(
                node=node,
                processor=Registry(owner=self),
                _session=Uid(),
                source=Registry(owner=self),
                transpiler=Registry(owner=self),
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            session = self._session()
            path = Path(specifier)

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
                **next(iter([a for a in args if js.type(a, "Object")]), {})
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

    use = Use()

    @use.source("use")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(
            self,
            path=None,
        ) -> dict:
            node = document.createElement("div")
            node.setAttribute("__path__", path.path)
            use.node.append(node)
            message = {}
            if meta.DEV:
                try:
                    text = anvil.server.call(f"_use", path.full)
                    message.update(test=True)
                except anvil.server.UplinkDisconnectedError as error:
                    text = self._get_text(node=node, path=path)
                except Exception as error:
                    raise ValueError(f"Invalid path: {path.full}. Error: {str(error)}")
            else:
                text = self._get_text(node=node, path=path)

            if meta.DEV:
                child = document.createElement("pre")
                child.textContent = text
                child.style.display = "none"
                node.append(child)

            return dict(node=node, text=text, **message)

        def _get_text(self, node=None, path=None) -> str:
            """Returns uncached text from sheet."""
            value = (
                js.getComputedStyle(node)
                .getPropertyValue(f"--__{self.key}__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid path: {path.full}.")
            text = js.atob(value[1:-1])
            return text

    @use.transpiler("css")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, node=None, path=None, test=False, text=None, **kwargs):
            """Returns transpiled value."""
            Future = use("use/future/future.py")
            link = document.createElement("link")
            link.rel = "stylesheet"
            link.setAttribute("path", path.path)

            ##href = f"{path.path}?content={use.js.btoa(text)}&encoding=base64"
            href = f"{path.path}?content={text}"
            link.href = href
            future = Future()

            def load(event):
                future()

            link.addEventListener("load", load, dict(once=True))

            document.head.append(link)

            future.wait()

            return link

    @use.transpiler("js")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, node=None, path=None, test=False, text=None, **kwargs):
            """Returns transpiled value."""
            module = js.module(text, path=path.path)
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
                if js.type(value, "Array", "Object"):
                    value = js.freeze(value)
                return value
            return module

    @use.transpiler("py")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

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
                    Base=Base,
                    anvil=anvil,
                    document=document,
                    js=js,
                    meta=meta,
                    window=window,
                    log=Log(path=path.full),
                    path=path,
                    text=text,
                    **kwargs,
                )

                ##log("type_name:", type(value).__name__)  ##

                if callable(value) and value.__name__ == "load":

                    def load(*args, **kwargs):
                        result = value(*args, **kwargs)
                        if isinstance(result, dict):
                            result = js.freeze(result)
                        return result

                    return dict(default="load", load=load)

                if isinstance(value, dict):
                    return dict(default="value", value=js.freeze(value))

                return dict(default="value", value=value)

            return dict(default="value", value=js.freeze(locals))

    @use.processor("json")
    class cls(Base):
        def __init__(self, **kwargs):
            from json import loads

            Base.__init__(self, _parse=loads, **kwargs)

        def __call__(self, result, *args, **kwargs):
            """."""
            if kwargs.get("key") != "text":
                return self._parse(result)

    # Set up test harness
    if meta.DEV:

        def test(path: str) -> None:
            """Runs test script."""
            text = anvil.server.call(f"_test", path)
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            main(
                use,
                log=Log(path=path),
                path=path,
                test=True,
            )

        @window.on()
        def keydown(event):
            if event.code == "KeyU" and event.shiftKey:
                stored = js.localStorage.getItem("__test__")
                path = window.prompt("Path:", stored)
                if path:
                    js.localStorage.setItem("__test__", path)
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
