"""
test/construct/construct.py
"""
def main(use, Base=None, log: callable = None, **kwargs) -> callable:
    class Construct(Base):
        def __init__(self, text: str = None, use: callable = None, **kwargs):
            Base.__init__(self)
            self._(text=text, use=use)

        def __call__(self, *args, **kwargs):
            locals = {}
            exec(self.text, {}, locals)
            main = locals.pop("main", None)

            annotations = main.__annotations__
            defaults = main.__defaults__
            doc = main.__doc__

            ##log('annotations:', annotations)
            ##log('defaults:', defaults)
            ##log('doc:', doc)

            



            if callable(main):
                meta = Base(doc=main.__doc__, returns=main.__annotations__.get('return'))
                kwargs.update(locals=locals)
                value = main(
                    self.use,
                    *args,
                    **kwargs,
                )
                return Base(value=value, meta=meta)

    text = use("use/future/future.py", text=True)
    ##log('text:', text)

    constructed = Construct(use=use, text=text)()
    log('constructed:', constructed)
   

    return Construct
