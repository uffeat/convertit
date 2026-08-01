def main(
    use,
    Path=None,
    anvil=None,
    console=None,
    document=None,
    js=None,
    meta=None,
    log=None,
    window=None,
    **kwargs,
):
    """."""

    print('client/test/test.py')

    registries = dict(source={}, transpile={}, process={})

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

    return use
