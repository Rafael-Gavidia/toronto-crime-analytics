# views/overview.py
# [US-14] Overview dashboard view

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

DOW_MAP = {
    "Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed",
    "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"
}

YELLOW_LIME_PALETTE = ["#9ccc65"]

YELLOW_LIME_HEATMAP_COLORSCALE = [
    [0.0,  "#fff8e1"],
    [0.33, "#ffd54f"],
    [0.66, "#cddc39"],
    [1.0,  "#689f38"],
]


def _card(label: str, value: str, subtitle: str = "", subtitle_color: str = "gray",
          value_size: str = "1.9rem", sub_size: str = "0.8rem") -> str:
    """Returns HTML for a single KPI card."""
    color_map = {"green": "#2e7d32", "red": "#c62828", "gray": "#666"}
    sub_color = color_map.get(subtitle_color, "#666")
    subtitle_html = (
        f'<div style="font-size:{sub_size};color:{sub_color};margin-top:4px">{subtitle}</div>'
        if subtitle else ""
    )
    return f"""
    <div style="
        background:#fff;
        border:1px solid #e0e0e0;
        border-radius:10px;
        padding:18px 20px;
        min-height:110px;
    ">
        <div style="font-size:0.75rem;color:#666;text-transform:uppercase;letter-spacing:0.05em">{label}</div>
        <div style="font-size:{value_size};font-weight:700;color:#1a1a1a;line-height:1.2;margin-top:6px">{value}</div>
        {subtitle_html}
    </div>
    """


def _build_kpi_cards(df: pd.DataFrame) -> None:
    """Render the four KPI metric cards."""

    total = len(df)

    # Peak crime hour — exclude hour 0 (known placeholder in police datasets)
    peak_hour_str = "N/A"
    is_midnight_peak = False
    if "OCC_HOUR" in df.columns:
        hour_counts = df["OCC_HOUR"].value_counts()
        peak_hour = int(hour_counts.idxmax())
        if peak_hour == 0:
            is_midnight_peak = True
            hour_counts_no_zero = hour_counts.drop(index=0, errors="ignore")
            real_peak = int(hour_counts_no_zero.idxmax()) if not hour_counts_no_zero.empty else 0
            peak_hour_str = f"{real_peak:02d}:00"
        else:
            peak_hour_str = f"{peak_hour:02d}:00"

    # Top division
    if "DIVISION" in df.columns:
        div_counts = df["DIVISION"].value_counts()
        top_div = div_counts.index[0]
        top_div_count = int(div_counts.iloc[0])
    else:
        top_div, top_div_count = "N/A", 0

    # Most common offence
    offence_col = (
        "OFFENCE" if "OFFENCE" in df.columns
        else "CSI_CATEGORY" if "CSI_CATEGORY" in df.columns
        else None
    )
    if offence_col:
        offence_counts = df[offence_col].value_counts()
        top_offence = offence_counts.index[0]
        top_offence_pct = round(offence_counts.iloc[0] / total * 100)
    else:
        top_offence, top_offence_pct = "N/A", 0

    # Year-over-year delta
    yoy_delta = None
    if "OCC_YEAR" in df.columns:
        years = sorted(df["OCC_YEAR"].dropna().unique())
        if len(years) >= 2:
            last_year = years[-1]
            prev_year = years[-2]
            count_last = len(df[df["OCC_YEAR"] == last_year])
            count_prev = len(df[df["OCC_YEAR"] == prev_year])
            if count_prev > 0:
                yoy_delta = round((count_last - count_prev) / count_prev * 100, 1)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(_card(
            "🛡 Total incidents",
            f"{total:,}",
            f"{yoy_delta:+.1f}% vs last year" if yoy_delta is not None else "",
            "green" if (yoy_delta is not None and yoy_delta < 0) else "red"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(_card(
            "🕐 Peak crime hour",
            peak_hour_str,
            "Highest incident rate"
        ), unsafe_allow_html=True)
        if is_midnight_peak:
            st.caption(
                "⚠️ **Note:** Hour 00:00 has the highest raw count but is excluded here. "
                "In Toronto police data, midnight is commonly used as a placeholder "
                "when the exact occurrence time is unknown."
            )

    with col3:
        st.markdown(_card(
            "📍 Top division",
            top_div,
            f"{top_div_count:,} incidents"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(_card(
            "⚠ Most common offence",
            top_offence,
            f"{top_offence_pct}% of all incidents"
        ), unsafe_allow_html=True)


def _build_folium_heatmap(df: pd.DataFrame) -> None:
    """Render folium-based geographic crime heatmap."""
    st.markdown("#### Crime heatmap — Toronto")
    st.caption("Incident density by location")

    coords_df = df[["LAT_WGS84", "LONG_WGS84"]].dropna()
    coords_df = coords_df[
        (coords_df["LAT_WGS84"] != 0) & (coords_df["LONG_WGS84"] != 0)
    ]

    if coords_df.empty:
        st.info("No coordinate data available for the selected filters.")
        return

    sample = coords_df.sample(min(len(coords_df), 20_000), random_state=42)
    heat_data = sample[["LAT_WGS84", "LONG_WGS84"]].values.tolist()

    m = folium.Map(
        location=[43.718, -79.38],
        zoom_start=11,
        tiles="CartoDB positron",
        prefer_canvas=True,
    )

    HeatMap(
        heat_data,
        radius=10,
        blur=15,
        min_opacity=0.3,
        gradient={0.2: "#ffffb2", 0.5: "#fd8d3c", 0.8: "#e31a1c", 1.0: "#800026"},
    ).add_to(m)

    st_folium(m, width="100%", height=400, returned_objects=[])


def _build_hourly_dow_heatmap(df: pd.DataFrame) -> None:
    """Render Plotly hourly x day-of-week heatmap — red/burgundy palette."""

    st.markdown("#### Hourly × day of week heatmap")
    st.caption("Incident count by hour and weekday")

    if "OCC_HOUR" not in df.columns or "OCC_DOW" not in df.columns:
        st.info("OCC_HOUR or OCC_DOW column not available.")
        return

    working = df[["OCC_HOUR", "OCC_DOW"]].copy()
    working["OCC_DOW"] = working["OCC_DOW"].str.strip().map(DOW_MAP)

    pivot = (
        working.groupby(["OCC_DOW", "OCC_HOUR"])
        .size()
        .reset_index(name="count")
        .pivot(index="OCC_DOW", columns="OCC_HOUR", values="count")
        .reindex(DAY_ORDER)
        .fillna(0)
    )

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{h}h" for h in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=YELLOW_LIME_HEATMAP_COLORSCALE,
        showscale=False,
        hoverongaps=False,
        hovertemplate="Day: %{y}<br>Hour: %{x}<br>Incidents: %{z:,}<extra></extra>",
        xgap=3,
        ygap=3,
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(side="top", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
    )

    st.plotly_chart(fig, use_container_width=True)


def show_overview(df: pd.DataFrame) -> None:
    """
    [US-14] Main overview view.
    Renders KPI cards, geographic heatmap, and hourly x DOW heatmap.
    All calculations delegated to src/ modules or local helpers above.
    No direct pandas aggregation in this function body.
    """
    st.markdown(
        "<h2 style='margin-bottom:2px'>Toronto Crime Analytics</h2>"
        f"<p style='color:#666;margin-top:0'>"
        f"{int(df['OCC_YEAR'].min()) if 'OCC_YEAR' in df.columns else '—'} – "
        f"{int(df['OCC_YEAR'].max()) if 'OCC_YEAR' in df.columns else '—'} · "
        f"All divisions · All offence types</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    _build_kpi_cards(df)

    st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        _build_folium_heatmap(df)

    with col_right:
        _build_hourly_dow_heatmap(df)