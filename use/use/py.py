def main(use, log: callable = None, **kwargs) -> callable:
    class Py(use.Base):
        def __init__(self, text: str = None, use: callable = use, **kwargs):
            self._(text=text, use=use, kwargs=kwargs)

        def __call__(self, *args, **kwargs):
            self.kwargs.update(**kwargs)
            kwargs = self.kwargs
            locals = {}
            exec(self.text, {}, locals)
            main = locals.pop("main", None)

            if callable(main):
                spec = next(
                    (v for v in main.__defaults__ if v and isinstance(v, dict)), None
                )
                # Make the function itself available to function body
                kwargs.update(self=main)
                # Make locals available to function body
                main.__dict__.update(locals)
                # Ensure that locals contains a config dict
                if not isinstance(locals.get("config"), dict):
                    main.__dict__.update(config=dict())

                value = main(
                    self.use,
                    *args,
                    **kwargs,
                )

                ##log("defaults:", main.__defaults__)  ##
                ##log("annotations:", main.__annotations__)  ##
                ##log("spec:", spec)  ##

                result = dict()
                if value is not None:
                    result.update(value=value)

                meta = dict()

                name = main.__name__
                if name != "main":
                    meta.update(name=name)

                config = main.__dict__.get("config")
                if config:
                    meta.update(config=config)

                doc = main.__doc__
                if doc:
                    meta.update(doc=doc)

                returns = main.__annotations__.get("return")
                if returns is not None:
                    meta.update(returns=returns)

                if spec:
                    meta.update(spec=spec)

                if meta:
                    result.update(meta=meta)

                return result


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
                        spec=spec,
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
