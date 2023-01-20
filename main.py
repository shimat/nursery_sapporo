import functools
import numpy as np
import pandas as pd
import streamlit as st
import folium
from typing import Iterable, Sequence

from const import WARDS, WARD_COLORS

# from loader import read_pdf
# from data_processing import combine_dataframes
from loader import read_csv, read_position_csv


# 申し込みが受け入れ予定以上のセルを赤くする
def select_over_requested(x: pd.io.formats.style.Styler) -> pd.io.formats.style.Styler:
    style_text = "background-color: rgb(255, 200, 200); font-weight:bold !important;"
    style_df = pd.DataFrame("", index=x.index, columns=x.columns)
    for age in range(6):
        mask = (x[f"{age}歳児受入予定"] < x[f"{age}歳児申込"]) | x[f"{age}歳児受入予定"].eq(0)
        style_df.loc[mask, [f"{age}歳児受入予定", f"{age}歳児申込"]] = style_text
    return style_df


# 座標に従って保育園の位置のマーカーを生成
def create_markers(df: pd.DataFrame, mode: str, selected_ages: Sequence[int]) -> Iterable[folium.Marker]:
    def make_li(row: pd.Series, age: int) -> str:
        requests, capacity = row[f"{age}歳児申込"], row[f"{age}歳児受入予定"]
        if requests is pd.NA or capacity is pd.NA:
            return f"<li>{age}歳: </li>"
        style: str = "color: red;" if requests >= capacity else ""
        return f"<li>{age}歳: <span style='{style}'>{requests} / {capacity}</span></li>"

    df = df.query("lat != 0 & lon != 0").copy()

    if mode == "申込超過":
        conditions: pd.Series[bool] = functools.reduce(
            # 年齢無選択なら、どこか空いていればよい(AND)、選択があればそれら全部が空いているか調べる
            lambda x, y: x & y if selected_ages == range(6) else x | y,
            [
                df[f"{age}歳児受入予定"].isna() | df[f"{age}歳児受入予定"].eq(0) | (df[f"{age}歳児受入予定"] <= df[f"{age}歳児申込"])
                for age in selected_ages
            ],
        )
        df.loc[:, "over"] = np.where(conditions, 1, 0)

    for index, row in df.iterrows():
        tooltip_text = popup_text = f"""
            <div style='font-size:medium; font-weight:bold;'>
              {index}: {row['施設名']}
            </div><div style='font-size:small;'>
              {row['区']} {row['住所']}
            </div>
            """
        popup_text += f"""
            <div style='font-size:small; margin-top:10px;'>
              申込数 / 受入数
              <ul>
                { "".join(make_li(row, a) for a in range(6))  }
              </ul>
            </div>
            """

        if mode == "区ごと":
            color = WARD_COLORS[row["区"]]
        else:
            color = "red" if row["over"] == 1 else "blue"
        yield folium.Marker(
            location=(row["lat"], row["lon"]),
            popup=folium.Popup(html=popup_text, min_width=200, max_width=300),
            tooltip=folium.Tooltip(tooltip_text),
            icon=folium.Icon(color=color),
            draggable=False,
        )


TITLE = "令和5年札幌市保育園申し込み状況"

st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)
st.markdown("https://kosodate.city.sapporo.jp/mokuteki/azukeru/hoiku/ninka/7656.html")

# dfs = read_pdf("R5ukeireyotesu1124_sasikae_1125_syuryo.pdf")
# df = combine_dataframes(dfs)
# df.to_csv("R5.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding="utf-8-sig")
df = read_csv("data/R5.csv")
df_pos = read_position_csv("data/latlon.csv")
df = pd.merge(df, df_pos, on="Index").drop(columns=["Index"])

col1, col2 = st.columns(2)
with col1:
    wards = st.multiselect("区", WARDS)
with col2:
    ages = st.multiselect("年齢 (受入予定が1人以上)", [f"{i}歳児" for i in range(6)])

if wards:
    df = df[df["区"].str.contains("|".join(wards), regex=True)]
if ages:
    ages = [f"{a}受入予定" for a in ages]
    target_rows = functools.reduce(lambda x, y: x | y, [df[a] for a in ages])
    df = df[target_rows > 0]

color_method = st.radio("色分け", ("区ごと", "申込超過"), horizontal=True)

map = folium.Map(location=(43.068665765741635, 141.35073227332813), zoom_start=11)
ages_int = tuple(int(a[0]) for a in ages) if ages else range(6)
for marker in create_markers(df, color_method, ages_int):
    marker.add_to(map)

# https://qiita.com/sentencebird/items/478e7151e952798c2bb8
st.components.v1.html(folium.Figure().add_child(map).render(), height=500)

st.text(f"ヒット: {len(df)}件")

df_show = df.drop(columns=["lat", "lon"])
style = df_show.style.highlight_null(color="lightgray")
style = style.apply(select_over_requested, axis=None)
st.dataframe(style)
