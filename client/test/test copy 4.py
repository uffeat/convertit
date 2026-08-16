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

    class Parcel(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _creators=Registry(owner=self), _data={}, **kwargs)

        def __call__(self, *args, **kwargs):
            """Registers creator."""
            return self._creators(*args, **kwargs)

        def __getitem__(self, key):
            """Returns item value."""
            if key in self._data:
                return self._data[key]
            creator = self._creators[key]
            if creator:
                value = creator(key)
                self._data[key] = value
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
                transpiler=Registry(owner=self)
                
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            # Enable setting options from JS
            kwargs.update(**next(iter([a for a in args if js.type(a, "Object")]), {}))
            path = Path(specifier)
            key = kwargs.get('key', 'value')

            if path.full in self._cache:
                # Retrieve parcel
                parcel = self._cache[path.full]
            else:
                parcel = Parcel()
                transpile = self.transpiler[path.type]
                if transpile:
                    transpile(parcel)

                
                self._cache[path.full] = parcel

            value = parcel[key]
            return value


    use = Use(
        Base=Base,
        Path=Path,
        Log=Log,
        anvil=anvil,
        document=document,
        js=js,
        meta=meta,
        window=window,
    )

    @use.transpiler('py')
    class py(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)

        def __call__(self, parcel):
            """."""


   
    log('use/ping.py:', use('use/ping.py'))


    class Text(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)

        def __call__(self, path=None):
            """."""

    class Py(Parcel):
        def __init__(self, **kwargs):
            Parcel.__init__(self, _cache={}, **kwargs)

        


    py = Py()

    @py('text')
    class text(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, key):
            """."""
            text = use.anvil.server.call(f"_use", key)
            log('text:', text)##
            return text

    log('use/ping.py:', py['use/ping.py'])

    

