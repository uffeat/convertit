"""
/parcels/path/test/test.py
"""


def main(use, **kwargs):
    """."""
    Path = use("@@/path/path.py")
   
    ##print("Path:", Path)  ##

    specifier = "@@/base/base.py"
    path = Path(specifier)

    print("path.source:", path.source)  ##
    print("path.path:", path.path)  ##
    print("path.parts:", path.parts)  ##
    print("path.parents:", path.parents)  ##
    print("path.file.name:", path.file.name)  ##
    print("path.file.stem:", path.file.stem)  ##
    print("path.file.type:", path.file.type)  ##
    print("path.file.types:", path.file.types)  ##






try:
    from utils import use
    main(use)
except:
    pass