# views/crime_by_hour.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.crime_by_hour import (
    get_crimes_polar,
    get_crimes_by_hour_and_dow,
    get_crimes_weekday_vs_weekend,
)

YELLOW_LIME_COLORSCALE = [
    
    [0.0,  "#fffde7"],  # very light yellow
    [0.33, "#fff176"],  # soft yellow
    [0.66, "#d4e157"],  # yellow-lime
    [1.0,  "#7cb342"],
]

DOW_SHORT = {
    "Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed",
    "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"
}


def _build_polar(df: pd.DataFrame) -> None:
    """Crime Clock — polar bar chart by hour."""
    st.markdown("#### Crime Clock")
    st.caption("Incident volume by hour of day (0–23). Each segment = one hour.")

    data = get_crimes_polar(df)

    fig = go.Figure(go.Barpolar(
        r=data["incident_count"],
        theta=data["angle"],
        width=[15] * 24,
        marker=dict(
            color=data["incident_count"],
            colorscale=YELLOW_LIME_COLORSCALE,
            showscale=False,
            line=dict(color="white", width=1),
        ),
        hovertemplate=(
            "<b>%{customdata}</b><br>"
            "Incidents: %{r:,}<extra></extra>"
        ),
        customdata=data["hour_label"],
    ))

    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                tickmode="array",
                tickvals=list(range(0, 360, 15)),
                ticktext=[f"{h:02d}h" for h in range(24)],
                direction="clockwise",
                rotation=90,
                tickfont=dict(size=11),
                gridcolor="#eee",
            ),
            radialaxis=dict(
                showticklabels=False,
                gridcolor="#eee",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=20, b=20),
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True)


def _build_hour_dow_heatmap(df: pd.DataFrame) -> None:
    """Hour x Day-of-Week heatmap with offence filter."""
    st.markdown("#### Incident Timing by Day and Hour")
    st.caption("Filter by offence type to reveal when specific crimes peak.")

    offence_options = ["All offences"]
    if "OFFENCE" in df.columns:
        top_offences = df["OFFENCE"].value_counts().head(15).index.tolist()
        offence_options += top_offences

    selected = st.selectbox("Filter by offence type:", offence_options)
    offence_filter = None if selected == "All offences" else selected

    pivot = get_crimes_by_hour_and_dow(df, offence=offence_filter)

    if pivot.empty:
        st.info("No data available for this selection.")
        return

    y_labels = [DOW_SHORT.get(d, d) for d in pivot.index.tolist()]

    hover_text = [
        [
            f"Day: {DOW_SHORT.get(day, day)}<br>Hour: {h:02d}:00<br>Incidents: {pivot.loc[day, h]:,}"
            for h in pivot.columns
        ]
        for day in pivot.index
    ]

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{h}h" for h in pivot.columns],
        y=y_labels,
        colorscale=YELLOW_LIME_COLORSCALE,
        showscale=False,
        hoverinfo="text",
        text=hover_text,
        xgap=3,
        ygap=3,
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(side="top", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        margin=dict(l=0, r=0, t=30, b=0),
        height=260,
    )

    st.plotly_chart(fig, use_container_width=True)


def _build_weekday_vs_weekend(df: pd.DataFrame) -> None:
    """Weekday vs Weekend average hourly crime comparison."""
    st.markdown("#### Weekday vs Weekend Hourly Pattern")
    st.caption(
        "Average incidents per hour on weekdays (Mon–Fri) vs weekends (Sat–Sun). "
        "Weekend crime shifts later into the night."
    )

    splits = get_crimes_weekday_vs_weekend(df)
    weekday = splits["weekday"]
    weekend = splits["weekend"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weekday["OCC_HOUR"],
        y=weekday["avg_incidents"],
        mode="lines+markers",
        name="Weekday",
        line=dict(color="#badc3d", width=2.5),
        marker=dict(size=6),
        hovertemplate="Hour: %{x:02d}:00<br>Avg incidents: %{y:,.1f}<extra>Weekday</extra>",
    ))

    fig.add_trace(go.Scatter(
        x=weekend["OCC_HOUR"],
        y=weekend["avg_incidents"],
        mode="lines+markers",
        name="Weekend",
        line=dict(color="#9cf072", width=2.5, dash="dash"),
        marker=dict(size=6),
        hovertemplate="Hour: %{x:02d}:00<br>Avg incidents: %{y:,.1f}<extra>Weekend</extra>",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(24)),
            ticktext=[f"{h:02d}h" for h in range(24)],
            tickfont=dict(size=10),
            gridcolor="#f0f0f0",
        ),
        yaxis=dict(gridcolor="#f0f0f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
    )

    st.plotly_chart(fig, use_container_width=True)


def show_crime_by_hour(df: pd.DataFrame) -> None:
    st.header("Crimes by Hour of Day")

    _build_polar(df)

    st.markdown("---")
    _build_hour_dow_heatmap(df)

    st.markdown("---")
    _build_weekday_vs_weekend(df)
import streamlit as st
from src.crime_by_hour import analyze_crime_by_hour

def show_crime_by_hour():

    st.title("Crime by Hour")

    st.write(
        "Crime by Hour analytics placeholder."
    )
