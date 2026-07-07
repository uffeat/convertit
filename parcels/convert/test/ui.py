"""
/parcels/convert/test/ui.py
"""


def main(use, console=None, document=None, **kwargs):
    ##print("kwargs:", kwargs)  ##

    x = use("@@/icons/x.svg")
    print("x:", x)



   
    page = use("@@/convert/convert.js").page
    print("page:", page)



