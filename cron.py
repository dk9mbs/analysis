import importlib
import os

def main():
    params={
        "dwd": {"sun_recent_file": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/sun/recent/stundenwerte_SD_00662_akt.zip"},
        "restapi": {"username":"root","password":"password", "url":"http://localhost:5000/api"}
    }


    for f in sorted(os.listdir(os.path.join(os.getcwd(), "tasks"))):
        print(f"Executing: {f}")
        if f.endswith("py") and f!='__init__.py':
            mod=f.replace(".py","")
            importlib.import_module(f"tasks.{mod}").execute(params)

    print(params)

main()
