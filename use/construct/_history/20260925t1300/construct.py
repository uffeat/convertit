def main(use: callable, Base: type = None, **kwargs):
    

    class construct(Base):
        def __init__(self):
            Base.__init__(self)

        def __call__(self, text: str, use: callable, *args, **kwargs):
            locals = {}
            exec(text, {}, locals)
            main = locals.pop('main', None)
            if callable(main):
                setattr(main, 'locals', locals)
                result = main(
                    use,
                    *args,
                    **kwargs,
                )
                return result

    return construct()
