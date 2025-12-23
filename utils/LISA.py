def lisa_map_px(data, col):
    import streamlit as st
    import numpy as np
    import plotly.express as px
    from libpysal.weights import Queen
    from esda import Moran_Local

    merged = data.copy()

    y = merged[col].values

    w = Queen.from_dataframe(merged)
    w.transform = 'r'

    moran_loc = Moran_Local(y, w)

    merged["LISA"] = moran_loc.Is

    # normalisasi 0–1
    a, b = 0, 1
    merged["LISA_norm"] = a + (
        (merged["LISA"] - merged["LISA"].min()) /
        (merged["LISA"].max() - merged["LISA"].min())
    )

    fig = px.choropleth(
        merged,
        geojson=merged.geometry,
        locations=merged.index,
        color="LISA_norm",
        color_continuous_scale="RdBu",
        range_color=(a, b),
        hover_data={col: True, "LISA": True},
        title="LISA Intensity Map"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig, use_container_width=True)

def lisa_map_cluster_px(data, col):
    import streamlit as st
    import numpy as np
    import plotly.express as px
    from libpysal.weights import Queen
    from esda import Moran_Local

    merged = data.copy()

    y = merged[col].values

    w = Queen.from_dataframe(merged)
    w.transform = 'r'

    moran_loc = Moran_Local(y, w)

    merged["LISA_clus"] = moran_loc.q

    cluster_labels = {
        1: "High-High",
        2: "Low-High",
        3: "Low-Low",
        4: "High-Low"
    }
    merged['LISA_clus'] = merged['LISA_clus'].map(cluster_labels)

    fig = px.choropleth(
        merged,
        geojson=merged.geometry,
        locations=merged.index,
        color="LISA_clus",
        category_orders={"LISA_show": [1, 4, 2, 3]},
        color_discrete_map={
            "High-High": "red",
            "Low-High": "lightblue",
            "Low-Low": "blue",
            "High-Low": "orange"
        },
        title="LISA Cluster Map"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig, use_container_width=True)
