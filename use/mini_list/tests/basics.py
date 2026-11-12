from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))



from test import use

MiniList = use("use/mini_list/mini_list.py")
print("MiniList:", MiniList)




