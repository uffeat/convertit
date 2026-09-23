def main(use: callable, Base: type = None, **kwargs):
    

    class construct(Base):
        def __init__(self):
            Base.__init__(self)

        def __call__(self, text: str, *args, **kwargs):
            locals = {}
            exec(text, {}, locals)
            main = locals.get('main')
            if callable(main):
                result = main(
                    use,
                    *args,
                    **kwargs,
                )
                return result

    return construct()
