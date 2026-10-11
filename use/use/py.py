def main(use, log: callable = None, **kwargs) -> callable:
    class Py(use.Base):
        def __init__(self, text: str = None, use: callable = use, **kwargs):
            self._(text=text, use=use, kwargs=kwargs)

        def __call__(self, *args, **kwargs) -> dict:

            locals = {}
            exec(self.text, {}, locals)
            main = locals.get("main")

           

            if callable(main):
                locals.pop("main", None)

                meta = use.dict()(
                    doc=main.__doc__,
                    returns=main.__annotations__.get("return"),
                    **locals.pop("meta", {}),
                    **next(
                        (v for v in main.__defaults__ if v and isinstance(v, dict)), {}
                    ),
                )

                main.__dict__.update(
                    meta=meta,
                )

               

                return use.dict()(
                    meta=meta if meta else None,
                    value=main(
                        self.use,
                        *args,
                        **use.dict()(**self.kwargs, **kwargs)(locals=locals, main=main),
                    ),
                )

            return locals

        

    return Py
