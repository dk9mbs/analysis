import importlib
import os
from config import CONFIG

def main():
    params=CONFIG


    for f in sorted(os.listdir(os.path.join(os.getcwd(), "tasks"))):
        print(f"Executing: {f}")
        if f.endswith("py") and f!='__init__.py':
            mod=f.replace(".py","")
            importlib.import_module(f"tasks.{mod}").execute(params)

    print(params)

main()
