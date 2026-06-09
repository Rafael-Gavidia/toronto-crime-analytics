import pandas as pd

class DataFilters:
    """
    [US-13] Centralized filtering logic for the interactive dashboard.
    Separating this from app.py ensures backend logic remains decoupled from UI.
    """

    @staticmethod
    def apply_multiselect_filter(df: pd.DataFrame, years: list, crimes: list) -> pd.DataFrame:
        """
        [US-13] Filters the dataframe based on selected years and crime types.
        Returns an empty dataframe if either selection list is empty to trigger UI alerts.
        """
        # Defensive Check: If the user clears all filters, return an empty dataframe
        if not years or not crimes:
            return pd.DataFrame(columns=df.columns)

        # Apply the intersection filter using pandas .isin()
        valid_rows = (
            df["OCC_YEAR"].isin(years) & 
            df["OFFENCE"].isin(crimes)
        )

        return df.loc[valid_rows].copy()