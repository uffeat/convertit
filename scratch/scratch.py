"""
/scratch/scratch.py
"""


def main(use, console=None, document=None, **kwargs):
    ##print("kwargs:", kwargs)  ##

   
    Foo = use("@@/foo/foo.py").Foo
    print("Foo:", Foo)

    ding = use("@@/ding/ding.py").ding
    print("ding:", ding())
   


