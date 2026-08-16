"""
test/use/foo/test/test.py
"""


def main(use, log=None, **kwargs):
    log("html:\n", use("use/foo/foo.html"), native=True)

    Foo, foo = use("use/foo/foo.py")
    log("Foo.foo:\n", Foo().foo)

    use("use/foo/bar/bar.py").bar()

    foo_json = use("use/foo/foo.json")
    log("foo_json:", foo_json)

    foo_json["foo"] = 43

    foo_json = use("use/foo/foo.json")
    log("foo_json:\n", foo_json)
    log("foo_json:\n", use("use/foo/foo.json", process=False))
