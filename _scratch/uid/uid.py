def Uid(*args, **kwargs) -> callable:
    """Returns callable for generating integer uid."""

    _ = {}

    class Uid:

        def __call__(self, *args, **kwargs) -> int:
            """Returns new uid."""
            value = _.get("value", -1) + 1
            _.update(value=value)
            return value

        @property
        def value(self) -> int:
            """Returns most recently generated uid."""
            return _.get("value", False)

    return Uid()


if __name__ == "__main__":

    def test():
        global Uid
        Uid = Uid()
        print("Uid.value:", Uid.value)
        print("Uid():", Uid())
        print("Uid.value:", Uid.value)
        print("Uid():", Uid())

    test()
