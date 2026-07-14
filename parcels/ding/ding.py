def main(use: callable, **kwargs) -> dict:

    def ding():
        foo = use("@@/foo/foo.py").foo
        foo()
        return "DING"

    return ding
