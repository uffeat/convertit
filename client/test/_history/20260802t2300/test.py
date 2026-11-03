def main(
    use,
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
