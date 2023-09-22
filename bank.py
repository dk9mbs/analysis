from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import json
import numpy as np


st.title("DK9MBS - GUV")

col1, col2 = st.columns(2)

with col1:
    analytic_year=st.number_input("Jahr", min_value=2000, max_value=2030, value=2023)

with col2:
    analytic_month=st.number_input("Monat", min_value=1, max_value=12, value=9)


df_all=pd.read_csv("/tmp/bank_item.csv")
times = pd.to_datetime(df_all.valutadatum)
#
# year with cat
#
pd_ser=df_all.groupby([times.dt.year, df_all.category_id], dropna=False).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'category_id']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_year_cat=tmp.query(f"year == {analytic_year}")

#
# year
#
pd_ser=df_all.groupby([times.dt.year],dropna=False).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name='year').join(tmp)
tmp=tmp.reset_index(drop=True)
df_year=tmp

#
# month without cat
#
pd_ser=df_all.groupby([times.dt.year, times.dt.month],dropna=False).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'month']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_month=tmp.query(f"year == {analytic_year}")



#df_month



#
# month wit cat
#
pd_ser=df_all.groupby([times.dt.year, times.dt.month, df_all.category_id],dropna=False).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'month', 'category_id']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_month_cat=tmp.query(f"year == {analytic_year} and month == {analytic_month}")




col1, col2 = st.columns(2)

with col1:
    st.markdown("#### GUV jährlich")
    st.bar_chart(data=df_year, x="year", y=["betrag"]  )

with col2:
    st.markdown(f"#### GUV monatlich {analytic_year}")
    st.bar_chart(data=df_month, x="month", y=["betrag"]  )

with col1:
    st.markdown(f"#### GUV monatlich nach Kategorien {analytic_month}.{analytic_year}")
    st.bar_chart(data=df_month_cat, x="category_id", y=["betrag"]  )

tmp=df_month_cat.query(f"month == {analytic_month}")
tmp

with col2:
    st.markdown(f"#### GUV jährlich nach Kategorien {analytic_year}")
    st.bar_chart(data=df_year_cat, x="category_id", y=["betrag"]  )

