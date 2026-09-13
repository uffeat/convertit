def main(use, **kwargs) -> callable:
    typeName = use("use/type/name.js")

    def parse(args: tuple, kwargs: dict):
        _kwargs = dict(
            next(
                iter(
                    [
                        a
                        for a in args[0:1]
                        if typeName(a) == "Object" or isinstance(a, dict)
                    ]
                ),
                {},
            )
        )
        ##log("_kwargs:", _kwargs)  ##
        if _kwargs:
            args = args[1:]
            kwargs.update(**_kwargs)
        return args

    return parse
