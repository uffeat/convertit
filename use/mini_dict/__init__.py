def MiniDict():
    from pathlib import Path
    import sys
    from .mini_dict import main

    sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
    from test import use

    return main(use)


MiniDict = MiniDict()
