def main(use, log: callable, path: str = None, **kwargs):
    """."""

    from anvil.js import import_from

    asset = use("use/asset/asset.py")

    print("asset:", asset("foo/foo.css"))
    print("type:", asset("foo/foo.css").content_type)
    print("text:", asset("foo/foo.css").get_bytes().decode("utf-8"))
    print("name:", asset("foo/foo.css").name)

    foo = import_from(f'/foo/foo.js?data={{"foo": 42}}').foo
    print("foo:", foo)

    Path = use("use/path/path.py")

    def main(*args, error: str = None, path: dict = None, query: dict = None, **kwargs):
        if error:
            raise Exception(error)
        path = Path(**path)
        log("path:", repr(path))  ##
        log("query:", query)  ##
        page = next(iter(path.parts[1:2]), None)
        log("page:", page)  ##

    return main
