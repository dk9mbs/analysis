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
    page_size=5000
    df_all=pd.DataFrame()
    reload_data=True

    if reload_data:
        while data!=[]:
            fetch=f"""
                <restapi type="select">
                    <table name="aprs_owntrack_log"/>
                </restapi>
            """
            data=json.loads(rest.read_multible("aprs_owntrack_log",fetch, page=page, page_size=page_size))

            df=pd.read_json(json.dumps(data))
            df_all = df_all.append(df, ignore_index=True)

            page+=1

        df_all.to_csv("/tmp/aprs_owntrack_log.csv", index=False)

