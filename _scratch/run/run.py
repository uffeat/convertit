def run(*args, **kwargs):

    def run(target: callable):
        print("annotations:", target.__annotations__)
        print("defaults:", target.__defaults__)

        annotations: dict = getattr(target, '__annotations__', {})
        defaults: tuple = getattr(target, '__defaults__', tuple())

        print("annotations:", annotations)
        print("defaults:", defaults)

        returns = annotations.get("return")
        ##print("returns:", returns)
        expects = next((a for a in defaults if isinstance(a, dict)), {}).get('expects')
        print("expects:", expects)
        
        if returns is dict:
            context = next((a for a in args if isinstance(a, dict)),{})



            result = target(**context)
            # Update context
            if isinstance(result, dict):
                [
                    context.pop(k, None) if v is None else context.update({k: v})
                    for k, v in result.items()
                ]
        else:
            result = target(*args, **kwargs)

        return result

    return run


if __name__ == "__main__":
    foo = 42

    context = dict(foo=foo, ding="DING", dong="DONG")

    @run(context)
    def _(config: dict = dict(expects=dict), ding: str=None, **kwargs) -> dict:
        ##print("kwargs:", kwargs)
        foo = 43
        return dict(bar=8, dong=None)

    print("foo:", foo)
    print("_:", _)
    print("context:", context)
