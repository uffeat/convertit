def main(use, **kwargs) -> callable:

    def scope(*args, **kwargs):
        
        def wrapper(target):
            return target(*args, **kwargs)

        return wrapper

    return scope
