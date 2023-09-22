import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

from clientlib import RestApiClient

def execute(params={}):
    df_all=pd.read_csv("/tmp/bank_item.csv")
    times = pd.to_datetime(df_all.valutadatum)
    #
    # year
    #
    pd_ser=df_all.groupby([times.dt.year, df_all.category_id]).betrag.sum()
    tmp=pd_ser.to_frame()

    tmp=tmp.index.to_frame(name=['year', 'category_id']).join(tmp)
    tmp=tmp.reset_index(drop=True)
    df_year=tmp
    #
    # month
    #
    pd_ser=df_all.groupby([times.dt.year, times.dt.month, df_all.category_id]).betrag.sum()
    tmp=pd_ser.to_frame()

    tmp=tmp.index.to_frame(name=['year', 'month', 'category_id']).join(tmp)
    tmp=tmp.reset_index(drop=True)
    df_month=tmp


    print(df_year)


    #
    # Save data
    #
    #df_hour.to_csv("/tmp/iot_diff_nord_sued_hour.csv", index=False)
    #df_day.to_csv("/tmp/iot_diff_nord_sued_day.csv", index=False)
    #df_month.to_csv("/tmp/iot_diff_nord_sued_month.csv", index=False)

