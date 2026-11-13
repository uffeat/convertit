from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))

from mini_dict import MiniDict



print('MiniDict:', MiniDict)