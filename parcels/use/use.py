def main(_use: callable, **kwargs) -> callable:
    """."""
    from anvil.js.window import (
        Blob,
        Object,
        URL,
        atob,
        console,
        document,
        getComputedStyle,
    )

    Base = _use("/base/base.py")
    Hook = _use("/use/hook.py")
    Path = _use("/path/path.py")

    meta = _use("/meta/meta.py")
    js = _use("/js/js.py")

    registries = dict(source={}, transpile={}, process={})

    class Use(Base):
        def __init__(self):
            Base.__init__(self)
            self._.update(cache={})

        def __call__(self, specifier: str, *args, **options):
            """."""
            raw = options.pop("raw", False)
            path = Path(specifier)
            hook = registries.get(path.source)
            if not hook:
                raise ValueError(f"Invalid source: {path.source}")
            result = hook(path, options=options)
            if raw:
                return result

            # Transpilation
            transpile = options.pop("transpile", True)
            if transpile:
                hook = registries.get(path.file.type)
                if hook:
                    transpiled = hook(path, result, *args, options=options)
                    if transpiled:
                        result = transpiled

            # Processing
            process = options.pop("process", True)
            if process:
                hook = registries.get(path.file.type)
                if hook:
                    processed = hook(path, result, *args, options=options)
                    if processed:
                        result = processed

            return result

        def hook(self, *keys):
            def register(cls):
                registry = registries.get(getattr(cls, "hook", None))
                hook = cls(owner=self)
                for key in keys:
                    registry[key] = hook

            return register

    use = Use()

    @use.hook("/")
    class cls(Hook):
        hook = "source"

        def __init__(self, owner=None):
            Hook.__init__(self, owner=owner)

        def __call__(self, path, *args, **kwargs) -> str:
            """Returns parcel text."""
            if path.path in self.cache:
                return self.cache[path.path]
            node = document.createElement("div")
            node.setAttribute("__path__", path.path)
            document.head.append(node)
            value = getComputedStyle(node).getPropertyValue("--__use__").strip()
            if not value:
                raise ValueError(f"Invalid {path}.")
            node.remove()
            result = atob(value[1:-1])
            self.cache[path.path] = result
            return result

    @use.hook("py")
    class cls(Hook):
        hook = "transpile"

        def __init__(self, owner=None):
            Hook.__init__(self, owner=owner)

        def __call__(self, path, text: str, *args, **kwargs) -> str:
            """Returns parcel text."""
            if not isinstance(text, str):
                return
            if path.path in self.cache:
                return self.cache[path.path]
            locals = {}
            exec(text, {}, locals)
            if "main" not in locals:
                raise ValueError(f"No 'main' in {path}.")
            main = locals["main"]
            result = main(self.owner, meta=meta, path=path, text=text)
            if isinstance(result, (dict, list)):
                result = Object.freeze(result)
            self.cache[path.path] = result
            return result
        
    @use.hook("js")
    class cls(Hook):
        hook = "transpile"

        def __init__(self, owner=None):
            Hook.__init__(self, owner=owner)

        def __call__(self, path, text: str, *args, **kwargs) -> str:
            """Returns parcel text."""
            if not isinstance(text, str):
                return
            if path.path in self.cache:
                return self.cache[path.path]
            
            js = self.owner("/js/js.py")
            
            


            self.cache[path.path] = result
            return result

    return use
