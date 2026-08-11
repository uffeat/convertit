"""
/parcels/convert/test/test.py
"""


def main(use, anvil=None, console=None, document=None, js=None, window=None, **kwargs):
    ##print("kwargs:", kwargs)  ##

    page = use("@@/convert/convert.js")
    console.log("page:", page)
