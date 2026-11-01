def Uid(*args, **kwargs) -> callable:
    """Returns callable for generating integer uid. Accepts optional seed and default value."""

    args = list(enumerate(args))

    _ = {
        **{
            "value": v - 1
            for i, v in args
            if isinstance(v, int) and not isinstance(v, bool) and not i
        },
        **{"default": v for i, v in args if i},
    }

    

    class Uid:

        def __call__(self, *args, **kwargs) -> int:
            """Returns new uid."""
            value = _.get("value", -1) + 1
            _.update(used=True, value=value)
            return value

        @property
        def value(self) -> int:
            """Returns most recently generated uid."""
            return _["value"] if _.get("used") else _.get("default", False)
            

    return Uid()



if __name__ == "__main__":

    

    def test():
        global Uid
        Uid = Uid(2, True)
        print("Uid.value:", Uid.value)
        print("Uid():", Uid())
        print("Uid.value:", Uid.value)
        print("Uid():", Uid())

    test()