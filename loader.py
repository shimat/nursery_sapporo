import pandas as pd

import streamlit as st


@st.experimental_memo
def read_pdf(file_name: str) -> list[pd.DataFrame]:
    import tabula

    dfs = tabula.read_pdf(
        file_name,
        lattice=True,
        pages="all",
        pandas_options={"header": [0, 1]},
    )
    return dfs


@st.experimental_memo
def read_csv(file_name: str) -> pd.DataFrame:
    dtypes = {}
    for a in range(6):
        dtypes[f"{a}歳児受入予定"] = dtypes[f"{a}歳児申込"] = "Int64"
    df = pd.read_csv(file_name, dtype=dtypes)
    return df


# @st.experimental_memo
def read_position_csv(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name)
    df = df.fillna(0)
    return df
