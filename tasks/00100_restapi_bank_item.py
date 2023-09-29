import pandas as pd
import requests
import json

from clientlib import RestApiClient

def _get_bank_item(rest) -> None:
    data=None
    page=0
    page_size=5000
    df_all=pd.DataFrame()
    reload_data=True

    if reload_data:
        while data!=[]:
            fetch=f"""
                <restapi type="select">
                    <table name="bank_item"/>
                </restapi>
            """
            data=json.loads(rest.read_multible("bank_item",fetch, page=page, page_size=page_size))
            print(f"reading page: {page} (pagesize: {page_size})")
            df=pd.read_json(json.dumps(data))

            df_all=pd.concat([df_all, df])
            #df_all = df_all.concat(df, ignore_index=True)

            page+=1

        df_all.to_csv("/tmp/bank_item.csv", index=False)

def _get_bank_account(rest):
    data=None
    page=0
    page_size=5000
    df_all=pd.DataFrame()
    reload_data=True

    if reload_data:
        while data!=[]:
            fetch=f"""
                <restapi type="select">
                    <table name="bank_account"/>
                </restapi>
            """
            data=json.loads(rest.read_multible("bank_account",fetch, page=page, page_size=page_size))
            print(f"reading page: {page} (pagesize: {page_size})")
            df=pd.read_json(json.dumps(data))

            df_all=pd.concat([df_all, df])
            page+=1

        df_all.to_csv("/tmp/bank_account.csv", index=False)


def execute(params={}):
    url=params['restapi']['url']
    apiusername=params['restapi']['username']
    apipassword=params['restapi']['password']
    rest=RestApiClient(url)
    rest.login(apiusername, apipassword)

    _get_bank_item(rest)
    _get_bank_account(rest)
