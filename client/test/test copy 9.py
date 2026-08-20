def main(
    Base: type = None,
    Log: type = None,
    Path: callable = None,
    anvil=None,
    document=None,
    js=None,
    log: callable = None,
    meta=None,
    path: str = None,
    window=None,
    server=None,
    **kwargs,
):
    """."""

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
                    ##print("Instatiating for:", key)  ##
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
                ##processor=self.Registry(owner=self),
                ##source=self.Registry(owner=self),
                ##transpiler=self.Registry(owner=self),
            )
            ##
            for key in ['processor', 'source', 'transpiler']:
                self._[key] = self.Registry(owner=self)
                ##self._[key] = (lambda: self.Registry(owner=self))()


        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            path = Path(specifier)
            if path.full in self._cache:
                parcel = self._cache[path.full]
            else:
                # Create minimal parcel
                parcel = dict()
                if path.source in self.source:
                    create = self.source[path.source]
                    updates = create(path=path, **parcel)
                    parcel.update(updates)
                self._cache[path.full] = parcel

            # Enable setting options from JS
            kwargs.update(**next(iter([a for a in args if js.type(a, "Object")]), {}))
            # XXX TODO key in specifier, so that kwargs can go directly to processors (not critical since key in kwargs does no harm)
            key = kwargs.get("key", "value")

            if key not in parcel:
                if path.type in self.transpiler:
                    # Enhance parcel
                    create = self.transpiler[path.type]
                    updates = create(path=path, **parcel)
                    parcel.update(updates)
                else:
                    key = "text"

            

            
            if path.type in self.processor:
                process = self.processor[path.type]
                processed = process(parcel, *args, **kwargs)
                if processed:
                    return processed

            result = parcel.get(key)
            return result

    use = Use(
        Base=Base,
        Path=Path,
        Log=Log,
        Registry=Registry,
        anvil=anvil,
        document=document,
        js=js,
        meta=meta,
        window=window,
    )

    @use.source("use")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, path=None, **kwargs) -> dict:
            result = dict()
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

            result.update(node=node, text=text, **message)
            return result

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

    @use.transpiler("py")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, path=None, text=None, **kwargs) -> dict:
            result = dict()
            locals = {}
            exec(text, {}, locals)
            main = locals.pop("main", None)
            if main:
                kwargs.update(locals)
                value = main(
                    use,
                    log=Log(path=path.full),
                    path=path,
                    text=text,
                    **kwargs,
                )
                if isinstance(value, dict):
                    value = use.js.freeze(value)
            else:
                value = use.js.freeze(locals)
            result.update(value=value)
            return result


    @use.transpiler("json")
    class cls(use.Base):
        def __init__(self, **kwargs):
            from json import loads
            use.Base.__init__(self, _parse=loads, **kwargs)

        def __call__(self, path=None, text=None, **kwargs) -> dict:
            def result():
                self._parse(text)
            
           
            return result


    @use.processor("XXXjson")
    class cls(use.Base):
        def __init__(self, **kwargs):
            from json import loads
            
            use.Base.__init__(self, _parse=loads, **kwargs)
           

        def __call__(self, parcel,**kwargs):
            """."""
            if kwargs.get('key') != 'text':
                result = self._parse(parcel['text'])

                return result


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
                log=Log(path=path),
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

    Foo, foo = use("use/foo/foo.py")
    log("foo:", foo())
    log("text:", use("use/foo/foo.py", key="text"))
    log("html:", use("use/foo/foo.html"))

    foo = use("use/foo/foo.json")
    log("json:", foo)

    use("use/foo/bar/bar.py").bar()
    log("node:", use("use/foo/bar/bar.py").node)
