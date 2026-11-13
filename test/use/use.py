import pathlib

cache = {}




class use:

    def __call__(self, specifier: str, *args, **kwargs):
        # Create
        if specifier in cache:
            parcel = cache[specifier]
        else:
            parcel = dict(text=(pathlib.Path.cwd() / specifier).read_text(encoding="utf-8").strip())
            config = {}
            if specifier.endswith(".py"):
                exec(parcel['text'], {}, parcel)
                parcel.update(
                    value=parcel.pop("main")(self, path=specifier, **parcel),
                )
                config.update(cache=True)
            if config.get('cache'):
                cache[specifier] = parcel
        
        
        return parcel.get(
            {True: k for k, v in kwargs.items() if v is True and k in parcel}.get(
                True, "value"
            ), "text"
        )


use = use()
