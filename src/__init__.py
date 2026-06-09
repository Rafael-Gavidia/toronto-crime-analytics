
"""
Toronto Crime Indicators Analytics Tool
Modular Python package for data cleaning and analysis.
"""

from .cleaner import clean_crime_data
from .data_loader import load_dataset
from .crime_by_hour import analyze_crime_by_hour

_all_ = [
    "clean_crime_data",
    "load_dataset",
    "analyze_crime_by_hour",
]

_version_ = "0.1.0"
_author_ = "Group 1"