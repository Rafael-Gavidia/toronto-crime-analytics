# views/premises.py

import streamlit as st
import pandas as pd
import plotly.express as px
from src.premises import get_premises_distribution, get_premises_offence_breakdown

AMBER_LIME_SEQUENCE = [
    "#558b2f",  # dark lime
    "#689f38",
    "#7cb342",
    "#9ccc65",
    "#c0ca33",
    "#d4e157",
    "#ffee58",
]



def _format_pct(pct: float) -> str:
    """Round percentage labels; show <0.1% for very small slices."""
    if pct < 0.1:
        return "<0.1%"
    return f"{pct:.1f}%"


def show_premises(df: pd.DataFrame):
    st.header("Premises Analysis")

    # --- Pie chart: overall distribution by premises type ---
    result = get_premises_distribution(df)
    total = result["incident_count"].sum()
    result = result.copy()
    result["pct"] = result["incident_count"] / total * 100
    result["pct_label"] = result["pct"].apply(_format_pct)

    pie_fig = px.pie(
        result,
        names="PREMISES_TYPE",
        values="incident_count",
        title="Crime Distribution by Premises Type",
        color_discrete_sequence=AMBER_LIME_SEQUENCE,
        custom_data=["pct_label"],
    )
    pie_fig.update_traces(
        texttemplate="%{customdata[0]}",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Incidents: %{value:,}<br>"
            "Share: %{customdata[0]}<extra></extra>"
        ),
    )
    pie_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("---")

    # --- 100% stacked bar: offence type breakdown per premises ---
    st.markdown("#### Crime Type Breakdown by Premises")
    st.caption(
        "Each bar represents one premises type and shows the proportion of each offence category. "
        "Reveals not just where crime happens, but what kind."
    )

    breakdown = get_premises_offence_breakdown(df, top_offences=6)

    if breakdown.empty:
        st.info("Not enough data to display offence breakdown.")
    else:
        # Order premises by total incident count (descending) for readability
        premises_order = (
            breakdown.groupby("PREMISES_TYPE")["incident_count"]
            .sum()
            .sort_values(ascending=True)  # ascending=True so largest is at top in horizontal chart
            .index.tolist()
        )

        bar_fig = px.bar(
            breakdown,
            x="percentage",
            y="PREMISES_TYPE",
            color="OFFENCE",
            orientation="h",
            title="Offence Type Breakdown by Premises (100% Stacked)",
            labels={
                "percentage": "Share (%)",
                "PREMISES_TYPE": "Premises Type",
                "OFFENCE": "Offence Type",
            },
            category_orders={"PREMISES_TYPE": premises_order},
            color_discrete_sequence=AMBER_LIME_SEQUENCE,
            custom_data=["incident_count", "OFFENCE"],
            text="percentage",
        )

        bar_fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate=(
                "<b>%{customdata[1]}</b><br>"
                "Premises: %{y}<br>"
                "Share: %{x:.1f}%<br>"
                "Incidents: %{customdata[0]:,}<extra></extra>"
            ),
        )

        bar_fig.update_layout(
            barmode="stack",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[0, 100], ticksuffix="%"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.35,
                xanchor="left",
                x=0,
            ),
            margin=dict(l=0, r=0, t=40, b=80),
            height=420,
        )

        st.plotly_chart(bar_fig, use_container_width=True)
import streamlit as st
from src.premises import get_premises_distribution, get_premises_percentage

def show_premises():

    st.title("Premises")

    st.write(
        "Premises placeholder."
    )
    
