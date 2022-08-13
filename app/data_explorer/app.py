import pandas as pd
import streamlit as st

@st.cache()
def get_data():
    df = pd.read_csv("prodeje.csv")
    df['scrape_date'] = pd.to_datetime(df['scrape_date'])
    df['scrape_date'] = df['scrape_date'].dt.strftime('%Y-%m')
    return df

df = get_data()


newdf = df.drop_duplicates(
  subset = ['odkaz', 'scrape_date'],
  keep = 'last').reset_index(drop = True)



kraje = df['kraj'].drop_duplicates()
typy_bytu = df['typBytu'].drop_duplicates()

filter_kraje = st.sidebar.multiselect('Kraj:', kraje)
filter_typBytu = st.sidebar.multiselect('Typ bytu:', typy_bytu)


filtered = df[(df["kraj"].isin(filter_kraje)) & (df["typBytu"].isin(filter_typBytu))]

df2 = filtered.groupby(["scrape_date"])['cena_Kc'].agg(['count','mean'])
df2 = df2.reset_index()

st.bar_chart(data=df2, x="scrape_date", y="count")
st.line_chart(data=df2, x="scrape_date", y="mean")

st.write(df2)