def main(use):
    Foo = use("/foo/foo.py").Foo

    foo = Foo()

    print("foo:", foo)
