import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_hourly_crime_plot(df: pd.DataFrame, offence_type: str = "Assault") -> go.Figure:
    """
    [SR-02] Generates a 24-hour chronological crime distribution bar chart.
    Ensures visual consistency, custom color palettes, and interactive properties.
    """
    # Filter dataset for the specific offence type if required
    filtered_df = df[df['MCI_CATEGORY'] == offence_type] if 'MCI_CATEGORY' in df.columns else df
    
    # Aggregate volume by hour
    hourly_counts = filtered_df.groupby('OCC_HOUR').size().reset_index(name='VOLUME')
    
    # Complete missing hours to ensure full 24-hour baseline visibility
    full_hours = pd.DataFrame({'OCC_HOUR': range(0, 24)})
    hourly_counts = pd.merge(full_hours, hourly_counts, on='OCC_HOUR', how='left').fillna(0)

    # Build the Plotly figure structure
    fig = px.bar(
        hourly_counts,
        x='OCC_HOUR',
        y='VOLUME',
        labels={'OCC_HOUR': 'Hour of Day (24h)', 'VOLUME': 'Crime Volume'},
        title=f"Chronological 24-Hour Distribution ({offence_type})",
        template='plotly_white',
        color_discrete_sequence=['#1f77b4']  # Standard institutional blue palette
    )
    
    # Apply precise interface dimensions and layout mutations
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.3)'),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode='x unified'
    )
    
    return fig


def create_filtered_crime_trend_plot(df: pd.DataFrame) -> go.Figure:
    """
    [SR-02] Generates a historical crime trend line chart using filtered multi-select data.
    Encapsulates all layout structures and color properties to prevent app views regression.
    """
    # Defensive Check: If the dataframe is empty (Zero-State), return a clean empty container with a message
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No Data Available - Please Select At Least One Filter Constraint",
            template="plotly_white"
        )
        return fig

    # Group filtered dataframe by Year and Offence type to calculate aggregate volume
    group_col = 'OFFENCE' if 'OFFENCE' in df.columns else ('MCI_CATEGORY' if 'MCI_CATEGORY' in df.columns else 'CSI_CATEGORY')
    trend_data = df.groupby(['OCC_YEAR', group_col]).size().reset_index(name='VOLUME')

    # Build the structural Plotly Express line chart
    fig = px.line(
        trend_data,
        x='OCC_YEAR',
        y='VOLUME',
        color=group_col,
        labels={'OCC_YEAR': 'Year', 'VOLUME': 'Incident Volume', group_col: 'Offence Type'},
        title="Interactive Historical Crime Trends by Selection Matrix",
        template='plotly_white'
    )

    # Enforce rigid responsive layout constraints and interactive behaviors
    fig.update_layout(
        xaxis=dict(dtick=1, tickmode='linear'),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.3)'),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='closest'
    )

    return fig


def create_filtered_premises_plot(df: pd.DataFrame) -> go.Figure:
    """
    [SR-02] Generates a horizontal bar chart for Premises distribution based on active filter states.
    Isolates precise graphical properties away from frontend UI layers.
    """
    # Defensive Check for Zero-State empty selections
    if df.empty or 'PREMISES_TYPE' not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            title="No Premises Data Available",
            template="plotly_white"
        )
        return fig

    # Aggregate counts for localized ranking presentation
    premises_counts = df['PREMISES_TYPE'].value_counts().reset_index()
    premises_counts.columns = ['PREMISES_TYPE', 'VOLUME']
    premises_counts = premises_counts.sort_values(by='VOLUME', ascending=True)

    # Build horizontal ranking visualization matrix
    fig = px.bar(
        premises_counts,
        x='VOLUME',
        y='PREMISES_TYPE',
        orientation='h',
        labels={'VOLUME': 'Crime Volume', 'PREMISES_TYPE': 'Premises Type'},
        title="Categorical Crime Distribution Across Active Premises",
        template='plotly_white',
        color_discrete_sequence=['#2ca02c']  # Maintained structural green identifier
    )

    fig.update_layout(
        margin=dict(l=100, r=40, t=60, b=40),
        hovermode='y unified'
    )

    return fig