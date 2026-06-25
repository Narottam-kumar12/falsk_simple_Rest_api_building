import os
import glob
import importlib

for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")):
    module = os.path.basename(f)[:-3]

    if module != "__init__":
        importlib.import_module(f"controller.{module}")