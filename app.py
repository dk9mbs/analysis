from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

from clientlib import RestApiClient

st.title("DK9MBS Sonnenschein Dauer Analyse")

st.markdown("## Einstellungen")
chart_date=st.date_input("Für welches Datum wollen Sie die Sonnenscheindauer analysieren?")
min_diff=st.number_input("Differenz in °C (detektiert Sonnenschein):", value=0.8, step=0.1, min_value=0.0)

x = datetime.strptime(str(chart_date), "%Y-%m-%d")

df_hour=pd.read_csv("/tmp/iot_diff_nord_sued_hour.csv").query(f"month == {x.month} and year == {x.year} and day == {x.day}")
df_hour['diff']=np.where(df_hour["diff"] <= min_diff, 0, df_hour["diff"])
df_hour['dwd_sunshine_duration']=df_hour['dwd_sunshine_duration']

df_day=pd.read_csv("/tmp/iot_diff_nord_sued_day.csv").query(f"month == {x.month} and year== {x.year}")

st.markdown ("## Stündliches Delta Nord - Süd vs. DWD")
st.write("Verglich zwischen der Sonnenscheindauer laut DWD (in der Einheit Sonnenscheindauer/10Min.) und der Differenz zwischen den Nord - Süd Temperatur Sensoren in °C")
st.area_chart(data=df_hour, 
    x="hour", y=["restapi_sunshine_duration", "dwd_sunshine_duration"]  )

#st.caption("diff: Differenz Nord - Süd Sensor in °C / dwd_sunshine_duration: Sonnenscheindauer laut DWD Station 662 in 10 Minuten")

df_hour[["hour","diff","restapi_sunshine_duration", "dwd_sunshine_duration"]]

#st.markdown ("## Tägliches Delta Nord - Süd")
#st.bar_chart(data=df_day, x="datetime", y="diff")

#
# MAP
#
df_track=pd.read_csv("/tmp/aprs_owntrack_log.csv")
st.map(df_track)
