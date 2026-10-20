def run(*args, **kwargs):

    def run(target: callable):
        result = target(*args, **kwargs)
        def Result():
            return result
        return Result

    return run




if __name__ == "__main__":
    foo = 42

    @run()
    def _(*args, **kwargs):
        print("args:", args)
        print("kwargs:", kwargs)
        foo = 43
        return 8

    print("foo:", foo)
    print("_():", _())

