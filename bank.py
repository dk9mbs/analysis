from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import json
import numpy as np


st.title("DK9MBS - GUV")

analytic_year=st.sidebar.number_input("Jahr", min_value=2000, max_value=2030, value=2023)
analytic_month=st.sidebar.number_input("Monat", min_value=1, max_value=12, value=9)

chk_show_income=st.sidebar.checkbox("Einnahmen auszeigen", value=True)
chk_show_costs=st.sidebar.checkbox("Kosten auszeigen", value=True)



df_all=pd.read_csv("/tmp/bank_item.csv")
times = pd.to_datetime(df_all.valutadatum)

df_all['datetime']=pd.to_datetime(df_all.valutadatum, format='%Y-%m-%dT%H:%M:%S')
df_all['year']=df_all.datetime.dt.year
df_all['month']=df_all.datetime.dt.month
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




tab1, tab2, tab3, tab4 = st.tabs(['Jahresvergleich','Monate (ausgewähltes Jahr)', 'Kategorien','Buchungen'])

tab1.markdown(f"##### Alle Jahre")
tab1.bar_chart(data=df_year, x="year", y=["betrag"]  )


tab2.markdown(f"##### Ausgewählter Monat ({analytic_year})")
tab2.bar_chart(data=df_month, x="month", y=["betrag"]  )


with tab3:
    col1 = st.columns(1)

    st.markdown(f"##### Ausgaben {analytic_year} nach Kategorien")

    tmp=df_year_cat.copy()

    if not chk_show_costs:
        tmp.query("betrag >= 0", inplace=True)

    if not chk_show_income:
        tmp.query("betrag <= 0", inplace=True)

    st.bar_chart(data=tmp, x="category_id", y=["betrag"]  )



with tab4:
    tmp=df_all[['beguenstigter_zahlungspflichtiger','betrag','category_id','year', 'month']]
    tmp.query(f"year == {analytic_year} and month =={analytic_month}", inplace=True)


    cfg={
        "betrag": st.column_config.NumberColumn(
            "Betrag",
            help="Betrag in Eur",
            format="%.2f€",
        ),
        "category_id": st.column_config.TextColumn(
            "Kategorie",
            help= "Kategorie"
        ),
        "year": st.column_config.NumberColumn(
            "Jahr",
            format="%i"
        ),
        "month": st.column_config.NumberColumn(
            "Monat",
            format="%i"
        )

    }
    st.dataframe(data=tmp, height=400, use_container_width=True, hide_index=True,column_config=cfg)

#tmp=df_month_cat.query(f"month == {analytic_month}")
#tmp


