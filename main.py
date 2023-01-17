import csv
import pandas as pd
import numpy as np
import streamlit as st
from data import read_pdf, combine_dataframes


TITLE = "令和5年札幌市保育園申し込み状況"
st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)
st.markdown("https://kosodate.city.sapporo.jp/mokuteki/azukeru/hoiku/ninka/7656.html")

dfs = read_pdf()
df = combine_dataframes(dfs)
df.to_csv("R5.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding="utf-8-sig")

col1, col2 = st.columns(2)
with col1:
    ward = st.selectbox(
        "区",
        (
            "全て",
            "中央区",
            "北区",
            "東区",
            "白石区",
            "厚別区",
            "豊平区",
            "清田区",
            "南区",
            "西区",
            "手稲区",
        ),
    )
with col2:
    age = st.selectbox("年齢", ("全て",) + tuple(f"{i}歳児" for i in range(6)))

if ward != "全て":
    df = df[df["区"] == ward]
# if age != "全て":
#    df = df[df[""]]
st.dataframe(df)

# df = df.reindex(columns=column_names)

# columns = df.iloc[0, :].values
# for c in range(6):
#    columns[2 + c*2] = df.iloc[0, 2+c] + df.iloc[1, 2 + c*2]
#    columns[2 + c*2+1] = df.iloc[0, 2+c] + df.iloc[1, 2 + c*2+1]
# df.columns = columns
# df.drop(index=df.index[[0, 1]], columns=df.columns[-1], inplace=True)
# df = df.reindex(columns=["", "", ""])

# for c in df.columns[2:]:
#    df[c] = df[c].astype("Int64")

# df = df.reset_index().drop("index", axis=1)
