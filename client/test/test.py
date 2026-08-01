def main(
    Base=None,
    Path=None,
    anvil=None,
    console=None,
    document=None,
    js=None,
    log=None,
    meta=None,
    window=None,
    **kwargs,
):
    """."""

    print("client/test/test.py")

    class Use:
        def __init__(self):
            """."""
            self.__dict__.update(__={})
            self._.update(cache={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, specifier: str):
            """."""
            path = Path(specifier)
            cache = self._["cache"]
            if path.path in cache:
                return cache[path.path]

            text = anvil.server.call("_use", path.path)

            locals = {}
            exec(text, {}, locals)
            main = locals["main"]
            result = main(
                self,
                Base=Base,
                Path=Path,
                anvil=anvil,
                console=console,
                document=document,
                js=js,
                log=log,
                meta=meta,
                path=path.path,
                window=window,
            )

            if isinstance(result, (dict, list)):
                result = js.freeze(result)

            cache[path.path] = result

            return result

    use = Use()


    use = use('/use/use.py')

    Hook = use("/use/hook.py")

    @use.hook("test")
    class cls(Hook):
        hook = "source"

        def __init__(self, owner=None):
            Hook.__init__(self, owner=owner)
            self._.update(cache={})

        def __call__(self, path, *args, **kwargs) -> str:
            """Returns code text."""
            cache = self._["cache"]
            if path.path in cache:
                result = cache[path.path]
                return result
            result = anvil.server.call("_test", path.path)
            
            cache[path.path] = result
            return result


    @window.on()
    def keydown(event):
        if event.code == "KeyU" and event.shiftKey:
            stored = js.localStorage.getItem("__test__")
            path = window.prompt("Path:", stored)
            if path:
                js.localStorage.setItem("__test__", path)
                use(f"test{path}")
