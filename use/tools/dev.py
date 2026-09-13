def main(use, **kwargs) -> callable:

    def dev(*args, **kwargs):

        def wrapper(target):
            if use.meta.DEV:
                return target(*args, **kwargs)

        return wrapper

    return dev
