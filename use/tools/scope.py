def main(use, **kwargs) -> callable:

    def scope(*args, **kwargs):
        
        def scope(target):
            return target(*args, **kwargs)

        return scope

    return scope
