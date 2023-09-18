import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

from clientlib import RestApiClient

def execute(params={}):
    sensor_id_shadow='GARTTEMP_NORD'
    sensor_id_sun='GARTTEMP01'

    df_all=pd.read_csv("/tmp/iot_sensor_data.csv")

    times = pd.to_datetime(df_all.created_on)
    pd_ser_hour=df_all.groupby([times.dt.year,times.dt.month, times.dt.day,times.dt.hour, df_all.sensor_id]).sensor_value.mean()
    tmp=pd_ser_hour.to_frame()

    tmp=tmp.index.to_frame(name=['year','month','day','hour','sensor_id']).join(tmp)
    tmp=tmp.reset_index(drop=True)

    df_g1=tmp.query("sensor_id == 'GARTTEMP01'")
    df_g2=tmp.query("sensor_id == 'GARTTEMP_NORD'")
    df_hour=pd.merge(df_g1, df_g2, on=["year","month","day","hour"], how='inner')
    df_hour['diff']=df_hour["sensor_value_x"]-df_hour["sensor_value_y"]
    df_hour['datetime']=pd.to_datetime(df_hour[['year', 'month','day', 'hour']])

    df_dwd=pd.read_csv("/tmp/dwd_sun.csv")
    df_hour=pd.merge(df_hour, df_dwd[['year','month','day','hour','SD_SO']], on=["year","month","day","hour"], how='inner')
    df_hour=df_hour.rename(columns={"SD_SO": "dwd_sunshine_duration"})

    #
    # per day
    #
    df_all=pd.read_csv("/tmp/iot_sensor_data.csv")
    times = pd.to_datetime(df_all.created_on)
    pd_ser_day=df_all.groupby([times.dt.year,times.dt.month, times.dt.day, df_all.sensor_id]).sensor_value.mean()
    tmp=pd_ser_day.to_frame()

    tmp=tmp.index.to_frame(name=['year','month','day','sensor_id']).join(tmp)
    tmp=tmp.reset_index(drop=True)

    df_g1=tmp.query(f"sensor_id == '{sensor_id_sun}'")
    df_g2=tmp.query(f"sensor_id == '{sensor_id_shadow}'")

    df_day=pd.merge(df_g1, df_g2, on=["year","month","day"], how='inner')
    df_day['diff']=df_day["sensor_value_x"]-df_day["sensor_value_y"]
    df_day['datetime']=pd.to_datetime(df_day[['year', 'month','day']])

    #
    # sum per month
    #
    df_all=pd.read_csv("/tmp/iot_sensor_data.csv")
    times = pd.to_datetime(df_all.created_on)
    pd_ser_month=df_all.groupby([times.dt.year,times.dt.month,times.dt.day, times.dt.hour, df_all.sensor_id]).sensor_value.mean()
    tmp=pd_ser_month.to_frame()

    tmp=tmp.index.to_frame(name=['year','month','day', 'hour','sensor_id']).join(tmp)
    tmp=tmp.reset_index(drop=True)    

    df_g1=tmp.query("sensor_id == 'GARTTEMP01'")
    df_g2=tmp.query("sensor_id == 'GARTTEMP_NORD'")

    df_month=pd.merge(df_g1, df_g2, on=["year","month","day", "hour"], how='inner')
    df_month['diff']=df_month["sensor_value_x"]-df_month["sensor_value_y"]
    df_month['diff']=np.where(df_month["diff"] <= 0, 0, df_month["diff"])

    print(df_month.groupby(["year", "month"])["diff"].sum())

    #
    # Save data
    #
    df_hour.to_csv("/tmp/iot_diff_nord_sued_hour.csv", index=False)
    df_day.to_csv("/tmp/iot_diff_nord_sued_day.csv", index=False)
    df_month.to_csv("/tmp/iot_diff_nord_sued_month.csv", index=False)

