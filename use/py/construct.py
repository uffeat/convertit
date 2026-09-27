def main(use, Base=None, log: callable = None, **kwargs) -> callable:
    class Construct(Base):
        def __init__(self, text: str = None, use: callable = None, **kwargs):
            Base.__init__(self)
            self._(text=text, use=use)

        def __call__(self, *args, **kwargs):
            locals = {}
            exec(self.text, {}, locals)
            main = locals.pop("main", None)

            if callable(main):

                main.__dict__.update(config=locals.pop("config", {}))

                kwargs.update(self=main)

                value = main(
                    self.use,
                    *args,
                    **kwargs,
                )

                meta = Base(
                    config=main.__dict__.get("config"),
                    doc=main.__doc__,
                    name=main.__name__ if main.__name__ != 'main' else None,
                    returns=main.__annotations__.get("return"),
                    
                )

                return Base(value=value, meta=meta)

    return Construct
