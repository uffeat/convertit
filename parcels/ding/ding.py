def main(use: callable, **kwargs):

    def ding():
        foo = use("@@/foo/foo.py").foo
        foo()
        return "DING"

    return ding
