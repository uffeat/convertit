"""
/parcels/foo/test/test.py
"""


def main(use, console=None, document=None, **kwargs):

    sheet = use("/foo/bar.css")
    console.log("sheet", sheet)

    link = use("/foo/bar.css", link=True)
    console.log("link", link)

   
    print("Foo:", use("/foo/foo.py"))
    console.log("Foo:", use("/foo/foo.js"))

    Foo = use("/foo/foo.py")

    foo = Foo()

    print("foo.foo:", foo.foo)

    element = document.createElement("h1")
    element.setAttribute("foo", "")
    element.setAttribute("bar", "")
    element.textContent = "Foo"
    document.body.append(element)
