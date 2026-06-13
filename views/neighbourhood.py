# views/neighbourhood.py

import streamlit as st
import pandas as pd
import plotly.express as px
from src.neighbourhood import get_neighbourhood_rankings, get_neighbourhood_trends

LIME_PALETTE = ["#a3e635"]

TREND_PALETTE = [
    "#558b2f",  # dark lime
    "#689f38",
    "#7cb342",
    "#9ccc65",
    "#c0ca33",
    "#d4e157",
    "#ffee58", 
]

def show_neighbourhood(df: pd.DataFrame):
    st.header("Neighbourhood Analysis")

    # --- Bar chart: Top N by total incidents ---
    top_n = st.slider("Top N Neighbourhoods", 5, 25, 10)
    rankings = get_neighbourhood_rankings(df, top_n=top_n)

    bar_fig = px.bar(
        rankings,
        x="incident_count",
        y="NEIGHBOURHOOD_158",
        orientation="h",
        title=f"Top {top_n} Neighbourhoods by Total Incidents",
        labels={"incident_count": "Incidents", "NEIGHBOURHOOD_158": "Neighbourhood"},
        color_discrete_sequence=LIME_PALETTE,
    )
    bar_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown("---")

    # --- Line chart: Year-over-year trend for top 5 ---
    st.markdown("#### Year-over-Year Crime Trend")
    st.caption(
        "5-year incident trend for the top 5 neighbourhoods by total crime volume. "
        "Use this to see whether high-crime areas are improving or worsening over time."
    )

    trends = get_neighbourhood_trends(df, top_n=5, years=5)

    if trends.empty:
        st.info("Not enough yearly data to display trends.")
    else:
        line_fig = px.line(
            trends,
            x="OCC_YEAR",
            y="incident_count",
            color="NEIGHBOURHOOD_158",
            markers=True,
            title="5-Year Crime Trend — Top 5 Neighbourhoods",
            labels={
                "OCC_YEAR": "Year",
                "incident_count": "Incidents",
                "NEIGHBOURHOOD_158": "Neighbourhood",
            },
            color_discrete_sequence=TREND_PALETTE,
        )
        line_fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
        line_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(dtick=1, tickformat="d"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.35,
                xanchor="left",
                x=0,
            ),
            margin=dict(l=0, r=0, t=40, b=80),
        )
        st.plotly_chart(line_fig, use_container_width=True)
