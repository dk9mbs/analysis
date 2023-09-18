import pandas as pd
import requests
import json

from clientlib import RestApiClient

def execute(params={}):
    url=params['restapi']['url']
    apiusername=params['restapi']['username']
    apipassword=params['restapi']['password']
    rest=RestApiClient(url)
    rest.login(apiusername, apipassword)

    data=None
    page=0
    page_size=50000
    df_all=pd.DataFrame()
    reload_data=False

    if reload_data:
        while data!=[]:
            fetch=f"""
                <restapi type="select">
                    <table name="iot_sensor_data"/>
                    <x_filter type="or">
                        <condition field="sensor_id" value="GARTTEMP01" operator="="/>
                        <condition field="sensor_id" value="GARTTEMP_NORD" operator="="/>
                    </x_filter>
                </restapi>
            """
            data=json.loads(rest.read_multible("iot_sensor_data",fetch, page=page, page_size=page_size))
            print(f"reading page: {page} (pagesize: {page_size})")
            df=pd.read_json(json.dumps(data))

            df_all = df_all.append(df, ignore_index=True)

            page+=1

        df_all.to_csv("/tmp/iot_sensor_data.csv", index=False)
        params['restapi_data']=df_all

