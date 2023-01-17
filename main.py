import functools
import pandas as pd
import streamlit as st
import pydeck as pdk

# from loader import read_pdf
# from data_processing import combine_dataframes
from loader import read_csv, read_position_csv


TITLE = "令和5年札幌市保育園申し込み状況"
WARDS = (
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
)

st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)
st.markdown("https://kosodate.city.sapporo.jp/mokuteki/azukeru/hoiku/ninka/7656.html")

# dfs = read_pdf("R5ukeireyotesu1124_sasikae_1125_syuryo.pdf")
# df = combine_dataframes(dfs)
# df.to_csv("R5.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding="utf-8-sig")
df = read_csv("data/R5.csv")
df_pos = read_position_csv("data/latlon.csv")
df = pd.merge(df, df_pos, on="施設名")

col1, col2 = st.columns(2)
with col1:
    wards = st.multiselect("区", WARDS)
with col2:
    ages = st.multiselect("年齢 (受入予定が1以上)", [f"{i}歳児" for i in range(6)])

if wards:
    df = df[df["区"].str.contains("|".join(wards), regex=True)]
if ages:
    ages = [f"{a}受入予定" for a in ages]
    target_rows = functools.reduce(lambda x, y: x | y, [df[a] for a in ages])
    df = df[target_rows > 0]

st.text(f"ヒット: {len(df)}件")


def select_over_requested(x: pd.io.formats.style.Styler) -> pd.io.formats.style.Styler:
    style_text = "background-color: rgb(255, 200, 200); font-weight:bold !important;"
    style_df = pd.DataFrame("", index=x.index, columns=x.columns)
    for age in range(6):
        mask = x[f"{age}歳児受入予定"] < x[f"{age}歳児申込"]
        style_df.loc[mask, [f"{age}歳児受入予定", f"{age}歳児申込"]] = style_text
    return style_df


ICON_DATA = {
    "url": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png",
    "width": 305,
    "height": 400,
    "anchorY": 400,
}
df["icon_data"] = ""
df.loc[:, ["icon_data"]] = ICON_DATA

style = df.style.highlight_null(color="lightgray")
style = style.apply(select_over_requested, axis=None)

st.dataframe(style)


st.pydeck_chart(
    pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(
            latitude=43.068665765741635,
            longitude=141.35073227332813,
            zoom=10,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "IconLayer",
                data=df,
                get_icon="icon_data",
                get_size=4,
                size_scale=15,
                get_position=["lon", "lat"],
                pickable=True,
            ),
        ],
        tooltip={"text": "{text}"},
    )
)
