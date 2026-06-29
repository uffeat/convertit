from anvil import Spacer
from anvil.js.window import (
    console,
    document,
)
from ..use import use

document.documentElement.dataset.bsTheme = "dark"





print("Base:", use("@@/base/base.py").Base)
print("Foo:", use("@@/foo/foo.py").Foo)

console.log("Base:", use("@@/base/base.js").Base)
console.log("Foo:", use("@@/foo/foo.js").Foo)




Foo = use("@@/foo/foo.py").Foo

foo = Foo()

print("foo.foo:", foo.foo)






# HACK Inherit from Spacer -> simplest component that allows server routing
class test(Spacer):
    def __init__(self, path: str = None, **query):
        print("path:", path)  ##
        print("query:", query)  ##
