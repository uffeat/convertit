def main(
    use: callable,
    Path: callable = None,
    anvil=None,
    document=None,
    js=None,
    meta=None,
    window=None,
    **kwargs,
) -> callable:
    """."""
    Hook = use("/use/hook.py")

    registries = dict(source={}, transpile={}, process={})


    pipe = []

    class PipeItem:
        def __init__(self):
            self.__dict__.update(__={})
            self._.update(registry={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: type, *args, **options):
            """."""
            registry: dict = self.__['registry']
            key: str = path.source
            hook = registry.get(key)
            return hook

        def hook(self, key, hook):
            """."""
            registry: dict = self.__['registry']
            registry[key] = hook


            

    pipe_item = PipeItem()


    class Source:
        def __init__(self):
            self.__dict__.update(__={})
            self._.update(registry={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, result=None):
            """."""
            if result is None:
                return 42












    pipe.append(pipe_item)

    class Use:
        def __init__(self):
            self.__dict__.update(__={})
            self._.update(cache={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, specifier: str, *args, **options):
            """."""
            ##print("specifier:", specifier)  ##
            raw = options.pop("raw", False)
            path = Path(specifier)



            for item in pipe:
                stuff = item(path)











            registry = registries["source"]
            hook = registry.get(path.source)
            if not hook:
                raise ValueError(f"Invalid source: {path.source}")
            result = hook(path, options=options)
            if raw:
                return result
            # Transpile
            transpile = options.pop("transpile", True)
            if transpile:
                registry = registries["transpile"]
                hook = registry.get(path.types)
                if hook:
                    transpiled = hook(path, result, *args, options=options)
                    if transpiled:
                        result = transpiled
            # Process
            process = options.pop("process", True)
            if process:
                registry = registries["process"]
                hook = registries.get(path.types)
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
            if meta.DEV:
                try:
                    result = anvil.server.call("_use", path.path)
                except:
                    result = self.get(path)
            else:
                result = self.get(path)

            self.cache[path.path] = result
            return result

        def get(self, path) -> str:
            """Returns uncached parcel text from sheet."""
            node = document.createElement("div")
            node.setAttribute("__path__", path.path)
            document.head.append(node)
            value = js.getComputedStyle(node).getPropertyValue("--__use__").strip()
            if not value:
                raise ValueError(f"Invalid {path}.")
            node.remove()
            result = js.atob(value[1:-1])
            return result

    @use.hook("py")
    class cls(Hook):
        hook = "transpile"

        def __init__(self, owner=None):
            Hook.__init__(self, owner=owner)

        def __call__(self, path, text: str, *args, **kwargs) -> str:
            """Returns parcel text."""
            # Type guard
            if not isinstance(text, str):
                return
            if path.path in self.cache:
                return self.cache[path.path]
            locals = {}
            exec(text, {}, locals)
            if "main" in locals:
                main = locals["main"]
                result = main(self.owner, meta=meta, path=path, text=text)
                if isinstance(result, (dict, list)):
                    result = js.freeze(result)
            else:
                result = js.freeze(locals)

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
            text = f"{text}\n//# sourceURL={path.path}"
            blob = js.new(js.Blob)([text], type="text/javascript")
            url = js.URL.createObjectURL(blob)
            module = js.use(url)
            js.URL.revokeObjectURL(url)
            # XXX TODO checks
            main = module.default
            result = main(self.owner, dict(path=path.path, text=text))
            type_name = js.type(result)
            if type_name == "Array" or type_name == "Object":
                result = js.freeze(result)
            self.cache[path.path] = result
            return result

    return use
