"""
/parcels/meta/test/test.py
"""


def main(use, console=None, document=None, js=None, **kwargs):
    """."""
   

    meta = use("@@/meta/meta.py")

    print('meta.DEV:', meta.DEV)
    print('meta.env:', meta.env)
    print('meta.origin:', meta.origin)

    
