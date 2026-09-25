from .base import Base

class Construct(Base):
    def __init__(self, text: str, use: callable):
        Base.__init__(self)
        self._(text=text, use=use)

    def __call__(self, *args, **kwargs):
        locals = {}
        exec(self.text, {}, locals)
        main = locals.pop("main", None)
        if callable(main):
            kwargs.update(locals=locals)
            result = main(
                self.use,
                *args,
                **kwargs,
            )
            return result

    
