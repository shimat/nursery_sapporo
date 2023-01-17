import itertools
import functools
from typing import Iterable
import numpy as np
import pandas as pd
import tabula
import streamlit as st


@st.experimental_memo
def read_pdf():
    dfs = tabula.read_pdf(
        "R5ukeireyotesu1124_sasikae_1125_syuryo.pdf",
        lattice=True,
        pages="all",
        pandas_options={"header": [0, 1]},
    )
    return dfs


def combine_dataframes(dfs: Iterable[pd.DataFrame]):
    def update(df: pd.DataFrame):
        ward = df.iloc[2, 0].replace("\r", "")
        if ward == "厚別区":
            df.iloc[3, 1:15] = df.iloc[3, 0:14]
            df.drop(index=df.index[[0, 1]], columns=df.columns[0], inplace=True)
        else:
            upper = df.iloc[2:3, 1:]
            lower = df.iloc[3:, :]
            upper.rename(
                columns={i + 1: i for i in range(upper.shape[1])}, inplace=True
            )
            df = pd.concat([upper, lower], axis=0)
            df.drop(columns=df.columns[-1], inplace=True)

        df.insert(1, "区", ward)
        df.columns = ["施設名", "区", "住所"] + list(
            itertools.chain.from_iterable(
                (f"{i}歳児受入予定", f"{i}歳児申込") for i in range(0, 6)
            )
        )
        df = df.reset_index().drop("index", axis=1)
        for c in df.columns[3:]:
            df[c] = np.floor(pd.to_numeric(df[c], errors="coerce")).astype("Int64")

        df["施設名"] = df["施設名"].str.replace("\r\n|\n|\r", " / ", regex=True)
        return df

    df_combined = functools.reduce(
        lambda all, d: pd.concat([all, update(d)]), dfs, None
    )
    return df_combined
