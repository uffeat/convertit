def main(use, Base=None, log: callable = None, **kwargs) -> callable:
    class Py(Base):
        def __init__(self, text: str = None, use: callable = use, **kwargs):
            Base.__init__(self)
            self._(text=text, use=use)

        def __call__(self, *args, **kwargs):
            locals = {}
            exec(self.text, {}, locals)
            main = locals.pop("main", None)

            if callable(main):
                # Make the function itself available to function body
                kwargs.update(self=main)
                # Make locals available to function body
                main.__dict__.update(locals)
                # Ensure that locals contains a config dict
                if not isinstance(locals.get("config"), dict):
                    main.__dict__.update(config=dict)

                value = main(
                    self.use,
                    *args,
                    **kwargs,
                )

                




                return Base.Dictionary(
                    value=value,
                    meta=Base.Dictionary(
                        config=main.__dict__.get("config"),
                        doc=self.parse(main.__doc__),
                        name=(
                            self.parse(main.__name__)
                            if main.__name__ != "main"
                            else None
                        ),
                        returns=main.__annotations__.get("return"),
                    ),
                )

        @staticmethod
        def parse(value):
            """."""
            if isinstance(value, str):
                value = value.strip()
                if (value.startswith("[") and value.endswith("]")) or (
                    value.startswith("{") and value.endswith("}")
                ):
                    import json

                    try:
                        value = json.loads(value)
                    except:
                        pass

            return value

    return Py
