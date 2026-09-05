def main(
    _use: callable,
    Base: type = None,
    log: callable=None,
    path: str = None,
    **kwargs,
) -> callable:
    """."""

    ##ping = _use('use/foo/ping.py')
    ##log('ping():', ping())
    ##log('ping():', ping())

    

    from anvil.server import call
    from anvil.js import import_from, new, window

    document = window.document

    class Use(Base):
        def __init__(self, *args, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path: str, *args, **kwargs):
            """Returns result from import engine."""
            if path in self._cache:
                parcel = self._cache[path]
            else:
                node = document.createElement("div")
                node.setAttribute("__path__", path[len("use") :])
                self.node.append(node)
                parcel = dict(node=node)
                if self.meta.DEV:
                    try:
                        text = call("_use", path)
                        parcel.update(test=True)
                    except:
                        text = self._get_text(node)
                else:
                    text = self._get_text(node)
                parcel.update(text=text)

                if path.endswith(".js"):
                    text = f"{text}\n//# sourceURL={path}"
                    blob = new(window.Blob, [text], dict(type="text/javascript"))
                    url = window.URL.createObjectURL(blob)
                    module = import_from(url)
                    window.URL.revokeObjectURL(url)
                    value = module.default(
                        self,
                        dict(path=path, **parcel),
                    )
                    if value is not None:
                        parcel.update(default="value", value=value)
                elif path.endswith(".py"):
                    locals = {}
                    exec(text, {}, locals)
                    value = locals["main"](
                        self,
                        Base=Base,
                        path=path,
                        **parcel,
                    )
                    if value is not None:
                        parcel.update(default="value", value=value)
                else:
                    parcel.update(default="text")

                self._cache[path] = parcel
            key = kwargs.get("key", parcel.get("default", "text"))
            result = parcel.get(key)
            return result

    use = Use(**_use._)

    return use
