import functools
import pandas as pd
import streamlit as st
import folium

from const import WARDS, WARD_COLORS

# from loader import read_pdf
# from data_processing import combine_dataframes
from loader import read_csv, read_position_csv


def select_over_requested(x: pd.io.formats.style.Styler) -> pd.io.formats.style.Styler:
    style_text = "background-color: rgb(255, 200, 200); font-weight:bold !important;"
    style_df = pd.DataFrame("", index=x.index, columns=x.columns)
    for age in range(6):
        mask = (x[f"{age}歳児受入予定"] < x[f"{age}歳児申込"]) | x[f"{age}歳児受入予定"].eq(0)
        style_df.loc[mask, [f"{age}歳児受入予定", f"{age}歳児申込"]] = style_text
    return style_df


TITLE = "令和5年札幌市保育園申し込み状況"

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

map = folium.Map(location=(43.068665765741635, 141.35073227332813), zoom_start=11)
for name, ward, addr, lat, lon in df[["施設名", "区", "住所", "lat", "lon"]].values:
    if lat == 0 and lon == 0:
        continue
    folium.Marker(
        location=(lat, lon),
        tooltip=f"{name}<br/>{ward} {addr}",
        icon=folium.Icon(icon="home", color=WARD_COLORS[ward]),
        draggable=False,
    ).add_to(map)

df.drop(columns=["lat", "lon"], inplace=True)
style = df.style.highlight_null(color="lightgray")
style = style.apply(select_over_requested, axis=None)
st.dataframe(style)

# https://qiita.com/sentencebird/items/478e7151e952798c2bb8
st.components.v1.html(folium.Figure().add_child(map).render(), height=500)
