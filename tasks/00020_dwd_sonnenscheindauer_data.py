import pandas as pd
import streamlit as st
from zipfile import ZipFile
import requests
import os


def execute(params={}):
    file=params['dwd']['sun_recent_file']
    loc_file="/tmp/sun.zip"
    extract_path="/tmp/dwd/"

    for (dir_path,_, files) in os.walk(extract_path):
        for f in files:
            del_file=os.path.join(dir_path, f)
            print(f"Removing file ... {del_file}")
            os.remove(del_file)

    r=requests.get(file, stream=True)

    open(loc_file, 'wb').write(r.content)
    with ZipFile(loc_file, 'r') as z:
        z.extractall(extract_path)

    import_file=""
    for (dir_path,_, files) in os.walk(extract_path):
        for f in files:
            if f.startswith("produkt"):
                import_file=os.path.join(dir_path, f)
                print(f"IMPORT: {import_file}")

    df_all=pd.read_csv(os.path.join(extract_path, import_file), sep=';')
    df_all['datetime']=pd.to_datetime(df_all.MESS_DATUM, format='%Y%m%d%H')
    df_all['year']=df_all.datetime.dt.year
    df_all['month']=df_all.datetime.dt.month
    df_all['day']=df_all.datetime.dt.day
    df_all['hour']=df_all.datetime.dt.hour
    df_all=df_all[['STATIONS_ID','SD_SO','datetime','year','month','day','hour']]
    print(df_all)

    df_all.to_csv("/tmp/dwd_sun.csv", index=True)



