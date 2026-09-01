def main(
    _use,
    log: callable = None,
    path: str = None,
    tools=None,
    **kwargs,
):
    """."""
    from types import ModuleType
    import anvil.js
    import anvil.server

    import_from = anvil.js.import_from
    new = anvil.js.new
    window = anvil.js.window
    document = window.document

    Base = tools.base.Base
    Log = tools.log.Log
    Path = tools.path.Path
    meta = tools.meta.meta

    ##log("dir(app):", dir(app))  ##
    # log("(app.__dict__:", app.__dict__)  ## This is really interesting!!!
    ##log("dir(meta):", dir(meta))  ##
    ##log("meta.__module__:", meta.__module__)  ##
    ##log("dir(tools):", dir(tools))  ##
    log("tools.__dict__:", tools.__dict__)  ##
    ##log("type(tools):", type(tools))  ##
    ##log("tools:", tools)  ##
   
    log("tools.meta.__dict__:", tools.meta.__dict__)  ##


   

    


    def parse_module(target: ModuleType) -> dict:
        """."""
        result = {}
        modules = [v for v in target.__dict__.values() if hasattr(v,  '__file__')]
        if modules:
            for module in modules:
                _result = parse_module(module)
                if isinstance(_result, dict):
                    result.update(_result)
        else:
            result['client_code/' + '/'.join(target.__file__.split('/')[2:])] = getattr(target, 'export', None)
        return result
        
        

    
    ##log('parsed:', parse_module(tools))
    ##log('parsed:', parse_module(tools.meta))
    


   

    window = anvil.js.window
    document = window.document

    

    class Use(Base):
        def __init__(self, **kwargs):

            Base.__init__(
                self,
                _cache={},
                **kwargs,
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            # Parse specifier
            path = Path(specifier)

            if path.full in self._cache:
                parcel = self._cache[path.full]
            else:
                node = document.createElement("div")
                node.setAttribute("__path__", path)
                parcel = dict(node=node)
                if meta.DEV:
                    try:
                        text = anvil.server.call(f"_use", path.full)
                        parcel.update(test=True)
                    except:
                        text = self._get_text(node)
                else:
                    text = self._get_text(node)
                parcel.update(text=text)
                # Transpile
                if path.type == "js":
                    text = f"{text}\n//# sourceURL={path.full}"
                    blob = new(window.Blob, [text], dict(type="text/javascript"))
                    url = window.URL.createObjectURL(blob)
                    module = import_from(url)
                    window.URL.revokeObjectURL(url)

                    value = module.default(
                        self,
                        dict(path=path.full, **parcel),
                    )
                    if value is not None:
                        parcel.update(default="value", value=value)
                elif path.type == "py":
                    locals = {}
                    exec(text, {}, locals)
                    value = locals["main"](
                        self,
                        log=Log(path.full),
                        path=path,
                        tools=tools,
                        **parcel,
                    )
                    if value is not None:
                        parcel.update(default="value", value=value)
                self._cache[path.full] = parcel

            result = parcel.get("value", parcel.get("text"))

            return result

        def add(self, *args):
            """."""
            module = next(iter([a for a in args if isinstance(a, ModuleType)]), None)
            if module:
                parsed = parse_module(module)
                for key, value in parsed.items():
                    self._cache[key] = dict(value=value)
            else:
                key, value = args
                self._cache[key] = dict(value=value)
            return self

        def _get_text(self, node) -> str:
            """Returns uncached text from sheet."""
            document.head.append(node)
            value = window.getComputedStyle(node).getPropertyValue(f"--__use__").strip()
            node.remove()
            text = window.atob(value[1:-1])
            return text

    use = Use()

    use.add(tools)

    _meta = use('client_code/tools/meta.py')
    log("same:",  _meta is meta)  ##




    ##
    log("ping:", use("use/foo/ping.py")())  ##
    log("ping:", use("use/foo/ping.js")())  ##
    ##log("ping:", use("use/ping.js")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##

    
    window = use("use/window/window.py")

    ##use = use("use/use/use.py")

    # Set up test harness
    if meta.DEV:

        def test(path: str) -> None:
            """Runs test script."""

            # XXX TODO Use Path and add js tests

            text = anvil.server.call(f"_use", path)
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            main(
                use,
                log=Log(path),
                path=path,
                test=True,
            )

        @window.on()
        def keydown(event):
            if event.code == "KeyU" and event.shiftKey:
                stored = window.localStorage.getItem("__test__")
                path = window.prompt("Path:", stored)
                if path:
                    window.localStorage.setItem("__test__", path)
                    test(path)

    # XXX TODO Move to tests

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

    ##_()

    ##log("ping:", use("use/ping.py")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##log("pong:", use("use/pong.py").pong())  ##
