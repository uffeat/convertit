"""
/parcels/tools/test/list/test.py
"""


def main(use, **kwargs):

    List = use("@@/tools/list.py")

    sequence = List(1, 2, 3)


    print("sequence:", sequence)
    
