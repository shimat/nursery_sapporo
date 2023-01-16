import pandas as pd
import numpy as np
import streamlit as st
from data import read_pdf, combine_dataframes


TITLE = "令和5年札幌市保育園申し込み状況"
st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)
st.markdown("https://kosodate.city.sapporo.jp/mokuteki/azukeru/hoiku/ninka/7656.html")

dfs = read_pdf()
df_combined = combine_dataframes(dfs)

# df.to_excel(f"{ward}.xlsx", index=None)


st.dataframe(df_combined)

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
