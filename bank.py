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
chk_show_only_main_account=st.sidebar.checkbox("Nur das Girokonto anzeigen", value=False)

analytic_comp_year=st.sidebar.number_input("Vergleichs Jahr", min_value=2000, max_value=2030, value=2023)



df_all=pd.read_csv("/tmp/bank_item.csv")
times = pd.to_datetime(df_all.valutadatum)

df_all['datetime']=pd.to_datetime(df_all.valutadatum, format='%Y-%m-%dT%H:%M:%S')
df_all['year']=df_all.datetime.dt.year
df_all['month']=df_all.datetime.dt.month

if not chk_show_costs:
    df_all.query("betrag >= 0", inplace=True)

if not chk_show_income:
    df_all.query("betrag <= 0", inplace=True)

if chk_show_only_main_account==True:
    df_all.query("account_id == 'DE65259501300173001058'", inplace=True)

#
# year with cat
#
pd_ser=df_all.groupby([times.dt.year, df_all.category_id], dropna=False).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'category_id']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_year_cat=tmp.query(f"year == {analytic_year}")
df_year_cat_comp=tmp.query(f"year == {analytic_comp_year}")

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

#
# month wit cat
#
pd_ser=df_all.groupby([times.dt.year, times.dt.month, df_all.category_id],dropna=False).betrag.sum()
tmp=pd_ser.to_frame()

tmp=tmp.index.to_frame(name=['year', 'month', 'category_id']).join(tmp)
tmp=tmp.reset_index(drop=True)
df_month_cat=tmp.query(f"year == {analytic_year} and month == {analytic_month}")


def compare_year_cat(df_year: pd.DataFrame, df_comp: pd.DataFrame):
    df=pd.merge(df_year, df_comp,on=["category_id"], how="outer")
    df['diff']=df['betrag_x']-df['betrag_y']
    return df


tab1, tab2, tab3, tab4 = st.tabs(['Jahresvergleich','Monate (ausgewähltes Jahr)', 'Kategorien','Buchungen'])

tab1.markdown(f"##### Alle Jahre")
tab1.bar_chart(data=df_year, x="year", y=["betrag"]  )


tab2.markdown(f"##### Ausgewählter Monat ({analytic_year})")
tab2.bar_chart(data=df_month, x="month", y=["betrag"]  )


with tab3:
    st.markdown(f"##### Ausgaben {analytic_year} nach Kategorien")
    st.bar_chart(data=df_year_cat, x="category_id", y=["betrag"]  )

    st.bar_chart(data=compare_year_cat(df_year_cat, df_year_cat_comp), x="category_id", y=["diff"]  )

    st.dataframe(data=compare_year_cat(df_year_cat, df_year_cat_comp) )


with tab4:
    chk_show_all_month_in_list=st.checkbox("Das komplette Jahr anzeigen", value=False)
    tmp=df_all[['beguenstigter_zahlungspflichtiger','betrag','category_id','year', 'month']]
    if chk_show_all_month_in_list:
        tmp.query(f"year == {analytic_year} and betrag != 0", inplace=True)
    else:
        tmp.query(f"year == {analytic_year} and month =={analytic_month} and betrag != 0", inplace=True)


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

    st.write(tmp['betrag'].sum())

#tmp=df_month_cat.query(f"month == {analytic_month}")
#tmp


