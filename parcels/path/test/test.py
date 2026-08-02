"""
/parcels/path/test/test.py
"""


def main(use, **kwargs):
    """."""
    Path = use("/path/path.py")
   
    ##print("Path:", Path)  ##

    specifier = "/foo/bar.py"
    path = Path(specifier)

    print("path.source:", path.source)  ##
    print("path.path:", path.path)  ##
    print("path.parts:", path.parts)  ##
    print("path.parents:", path.parents)  ##
    print("path.name:", path.name)  ##
    print("path.stem:", path.stem)  ##
    print("path.type:", path.type)  ##
    print("path.types:", path.types)  ##






try:
    from utils import use
    main(use)
except:
    pass