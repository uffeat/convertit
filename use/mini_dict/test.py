import sys
from pathlib import Path
from types import ModuleType
import tests

sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))

from use.mini_dict import MiniDict

from test import use

##MiniDict = use('use/mini_dict/mini_dict.py')


tests = {
    k: v
    for k, v in tests.__dict__.items()
    if isinstance(k, str) and not k.startswith("_") and isinstance(v, ModuleType)
}

results = {
    name: test(MiniDict)
    for name, test in {
        k: getattr(v, "test") for k, v in tests.items() if hasattr(v, "test")
    }.items()
}
print("results:", results)


results = {
    name: main(use)
    for name, main in {
        k: getattr(v, "main") for k, v in tests.items() if hasattr(v, "main")
    }.items()
}
print("results:", results)
