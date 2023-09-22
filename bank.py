from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import json
import numpy as np


st.title("DK9MBS")

st.markdown("## Einstellungen")


df_all=pd.read_csv("/tmp/bank_item.csv")
times = pd.to_datetime(df_all.valutadatum)
#
# year with cat
#
pd_ser=df_all.groupby([times.dt.year, df_all.category_id]).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'category_id']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_year_cat=tmp.query("year == 2023")

#
# year
#
pd_ser=df_all.groupby([times.dt.year]).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name='year').join(tmp)
tmp=tmp.reset_index(drop=True)
df_year=tmp

#
# month without cat
#
pd_ser=df_all.groupby([times.dt.year, times.dt.month]).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'month']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_month=tmp.query("year == 2023")

st.bar_chart(data=df_year, x="year", y=["betrag"]  )
st.bar_chart(data=df_month, x="month", y=["betrag"]  )
st.bar_chart(data=df_year_cat, x="category_id", y=["betrag"]  )
#df_year

