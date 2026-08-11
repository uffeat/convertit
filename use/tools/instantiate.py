def main(use, **kwargs) -> callable:

    def instantiate(*args, **kwargs) -> callable:
        def result(cls):
            if "__init__" in cls.__dict__:
                return cls(*args, **kwargs)
            return cls()

        return result

    return instantiate
