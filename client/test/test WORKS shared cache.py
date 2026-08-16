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
        def __init__(self, owner=None):
            Base.__init__(
                self,
                owner=owner,
                _registry={},
            )

        def __call__(self, key, *args) -> callable:
            """Registers callable."""
            # NOTE Register mutable to allow lazy instantiation
            value = args[0] if args else None
            if value:
                # Not used as decorator
                if isinstance(value, type):
                    value = value(key=key, owner=self)
                self._registry[key] = dict(value=value)
                return value

            
            def register(value: type) -> callable:
                """Decorator."""
                self._registry[key] = dict(value=value)
                return value

            return register

        def __getitem__(self, key):
            """Returns registree instance."""
            source = self._registry.get(key)
            if source:
                value = source["value"]
                if isinstance(value, type):
                    value = value(key=key, owner=self)
                    source["value"] = value
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
            # Update state
            self._.update(
                node=node,
                processor=self.Registry(owner=self),
                source=self.Registry(owner=self),
                transpiler=self.Registry(owner=self),
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            # Enable setting options from JS
            kwargs.update(**next(iter([a for a in args if js.type(a, "Object")]), {}))
            path = Path(specifier)
            # Get result
            if path.full in self._cache:
                # Retrieve result
                parcel: dict = self._cache[path.full]
            else:
                # Build result
                source = self.source[path.source]
                if not source:
                    raise ValueError(f"Invalid source: {path.source}.")
                parcel: dict = source(path)
                transpile = self.transpiler[path.type]
                if transpile:
                    value = transpile(path=path, **parcel)
                    parcel.update(value=value)
                else:
                    text = parcel.pop("text")
                    parcel.update(value=text)
                self._cache[path.full] = parcel
            # Process (use for for uncached post-processing/transpilation)
            process = kwargs.get("process", True)
            if process:
                processor = self.processor[path.type]
                if processor:
                    processed = processor(**parcel)
                    if processed is not None:
                        return processed
            # Return from parcel
            if kwargs.get("raw", False):
                # Handle raw
                key = "text" if "text" in parcel else "value"
            else:
                key = kwargs.get("key", "value")
            return parcel.get(key)

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

        def __call__(self, path) -> dict:
            """Returns parcel."""
            parcel = dict()
            node = use.document.createElement("div")
            node.setAttribute("__path__", path.path)
            use.node.append(node)
            message = {}
            if use.meta.DEV:
                try:
                    text = use.anvil.server.call(f"_{self.key}", path.full)
                    message.update(test=True)
                except use.anvil.server.UplinkDisconnectedError as error:
                    text = self._get_text(node=node, path=path)
                except Exception as error:
                    raise ValueError(f"Invalid path: {path.full}. Error: {str(error)}")

            else:
                text = self._get_text(node=node, path=path)
            parcel.update(node=node, text=text, **message)
            return parcel

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
            Future = use('use/future/future.py')
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

        def __call__(self, node=None, path=None, test=False, text=None, **kwargs):
            """Returns transpiled value."""
            locals = {}
            exec(text, {}, locals)
            main = locals.pop("main", None)
            if main:
                value = main(
                    use,
                    log=Log(path=path.full),
                    node=node,
                    path=path,
                    test=test,
                    **locals,
                )
                if isinstance(value, dict):
                    value = use.js.freeze(value)
            else:
                value = use.js.freeze(locals)
            return value

    @use.processor("json")
    class cls(use.Base):
        def __init__(self, **kwargs):
            """."""
            from json import loads as _parse

            use.Base.__init__(self, _parse=_parse, **kwargs)

        def __call__(self, value: str = None, **kwargs):
            """Returns parsed json."""
            return self._parse(value)

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


    
