# views/division.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.division import get_division_crime_counts, get_division_yearly_trends

YELLOW_LIME_PALETTE = ["#a3e635"]

YELLOW_LIME_HEATMAP_COLORSCALE = [
    [0.0,  "#fffde7"],  # very light yellow
    [0.33, "#fff176"],  # soft yellow
    [0.66, "#d4e157"],  # yellow-lime
    [1.0,  "#7cb342"],  # deep lime green
]


def show_division(df: pd.DataFrame):
    st.header("Division Performance")

    # --- Bar chart: total incidents per division ---
    counts = get_division_crime_counts(df)
    # Remove Unknown for cleaner visuals
    counts = counts[counts["DIVISION"] != "Unknown"].copy()

    bar_fig = px.bar(
        counts,
        x="DIVISION",
        y="incident_count",
        title="Total Crime Volume by Division",
        labels={"DIVISION": "Division", "incident_count": "Incidents"},
        color_discrete_sequence=YELLOW_LIME_PALETTE,
        text="incident_count",
    )
    bar_fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    bar_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(categoryorder="total descending"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown("---")

    # --- Heatmap: Division x Year ---
    st.markdown("#### Crime Activity Heatmap — Division × Year")
    st.caption(
        "Incident volume per division per year (2020–2026). "
        "Darker cells indicate higher activity. Reveals which divisions are trending up or down."
    )

    col1, col2 = st.columns(2)
    with col1:
        year_from = st.number_input("From year", min_value=2000, max_value=2025, value=2020, step=1)
    with col2:
        year_to = st.number_input("To year", min_value=2001, max_value=2026, value=2026, step=1)

    if year_from >= year_to:
        st.warning("'From year' must be less than 'To year'.")
        return

    pivot = get_division_yearly_trends(df, year_from=int(year_from), year_to=int(year_to))

    if pivot.empty:
        st.info("No data available for the selected year range.")
        return

    # Build hover text matrix
    hover_text = [
        [f"Division: {div}<br>Year: {year}<br>Incidents: {pivot.loc[div, year]:,}"
         for year in pivot.columns]
        for div in pivot.index
    ]

    heatmap_fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(y) for y in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=YELLOW_LIME_HEATMAP_COLORSCALE,
        showscale=True,
        colorbar=dict(title="Incidents", thickness=14, len=0.8),
        hoverinfo="text",
        text=hover_text,
        xgap=3,
        ygap=3,
    ))

    heatmap_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(side="top", tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12), autorange="reversed"),
        margin=dict(l=0, r=0, t=30, b=0),
        height=max(300, len(pivot.index) * 38),
    )

    st.plotly_chart(heatmap_fig, use_container_width=True)
