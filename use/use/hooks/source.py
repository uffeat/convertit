def main(
    use: callable,
    Base: type = None,
    **kwargs,
):
    """."""
    
    

    

    @use.creator("source", "use")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """Returnsnode and text updates."""
            result = {}
            node = document.createElement("div")
            node.setAttribute("__path__", path.relative)
            use.node.append(node)
            if use.meta.DEV:
                from anvil.server import call

                try:
                    text = call("_use", path.path)
                    result.update(test=True)
                except:
                    text = self._get_text(node)
            else:
                text = self._get_text(node)
            result.update(node=node, text=text)
            return result

        def _get_text(self, node) -> str:
            """Returns uncached text from sheet."""
            value = window.getComputedStyle(node).getPropertyValue("--__path__").strip()
            text = window.atob(value[1:-1])
            return text

    @use.creator("type", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                Construct = use.package.tools.Construct
                Log = use.package.client.tools.Log
                result = {}
                value = Construct(text=text, use=use)(
                    Base=Base,
                    log=Log(path.path),
                    path=path.path,
                    **parcel,
                )
                if value is not None:
                    result.update(default="value", value=value)
                return result

    @use.creator("type", "js")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._.update(meta=window.Object.freeze(dict(use.meta)))

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                Construct = use.package.client.tools.Construct
                result = {}
                value = Construct(path=path.path, text=text, use=use)(
                    path=path.path, **parcel
                )
                if value is not None:
                    result.update(default="value", value=value)
                return result

    @use.processor("js", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(
            self,
            args=None,
            kwargs=None,
            path=None,
            result=None,
        ):
            """."""

            if hasattr(result, "keys"):
                return window.Object.freeze(result)

    @use.processor("json")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(
            self,
            args=None,
            kwargs=None,
            path=None,
            result=None,
        ):
            """."""
            if not kwargs.get("key") == "text" and isinstance(result, str):
                import json

                return json.loads(result)

    ##Path = use("use/path/path.py")
    ##log("Path:", Path)  ##

    return use
