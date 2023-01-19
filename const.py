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

ICON_COLORS = (
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "darkred",
    "darkblue",
    "darkgreen",
    "darkpurple",
    "lightgray",
    "lightred",
    "cadetblue",
    "beige",
    "white",
    "pink",
    "gray",
    "black",
    "lightblue",
    "lightgreen",
)

WARD_COLORS = {name: ICON_COLORS[i] for i, name in enumerate(WARDS)}
