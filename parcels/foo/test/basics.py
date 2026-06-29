"""
/parcels/foo/test/basics.py
"""


def main(use, console=None, document=None, **kwargs):

    sheet = use("@@/foo/bar.css")
    console.log("sheet", sheet)

    link = use("@@/foo/bar.css", link=True)
    console.log("link", link)

    print("Base:", use("@@/base/base.py").Base)
    print("Foo:", use("@@/foo/foo.py").Foo)

    console.log("Base:", use("@@/base/base.js").Base)
    console.log("Foo:", use("@@/foo/foo.js").Foo)

    Foo = use("@@/foo/foo.py").Foo

    foo = Foo()

    print("foo.foo:", foo.foo)

    element = document.createElement("h1")
    element.setAttribute("foo", "")
    element.setAttribute("bar", "")
    element.textContent = "Foo"
    document.body.append(element)
