import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
target = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(target, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"), os.path.join(target, "entry.png"))
