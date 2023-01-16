import pandas as pd
import tabula
import streamlit as st


@st.experimental_memo
def read_pdf():
    dfs = tabula.read_pdf(
        "R5ukeireyotesu1124_sasikae_1125_syuryo.pdf",
        lattice=True,
        pages="all",
        pandas_options={"header": [0, 1]}
    )
    return dfs


dfs = read_pdf()
for df in dfs:
    ward = df.iloc[:, 0].str.replace("\r", "")[2]
    print(ward)

    upper = df.iloc[0:3, 1:]
    lower = df.iloc[3:, :]
    replace_table = {i+1: i for i in range(upper.shape[1])}
    upper = upper.rename(columns=replace_table)

    df = pd.concat([upper, lower], axis=0)
    print(df)
    print(df.iloc[0:2, :])

    columns = df.iloc[0, :]
    for c in range(6):
        columns[2 + c*2] = df.iloc[0, 2+c] + df.iloc[1, 2 + c*2]
        columns[2 + c*2+1] = df.iloc[0, 2+c] + df.iloc[1, 2 + c*2+1]
    df.columns = columns
    df.drop(index=df.index[[0, 1]], columns=df.columns[-1], inplace=True)

    print(df)
    for c in df.columns[2:]:
        df[c] = df[c].astype("Int64")
    df = df.reset_index().drop("index", axis=1)

    st.dataframe(df)
    # df.to_excel(f"{ward}.xlsx", index=None)
    break
