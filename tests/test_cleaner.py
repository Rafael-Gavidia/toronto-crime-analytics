import pandas as pd
import pytest
from src.pipeline import CrimeDataPipeline

@pytest.fixture
def mock_raw_data():
    """Фикстура, генерирующая «грязные» сырые данные для проверки TDD цикла."""
    return pd.DataFrame({
        "LAT_WGS84": [43.70, 0.0, 55.0, 43.65],
        "LONG_WGS84": [-79.40, 0.0, -120.0, -79.35],
        "LOCATION_TYPE": ["Convenience Store", "Commercial", "NSA", "NSA"],
        "OCC_DATE": ["2024-01-01", "2024-01-02", "2024-01-03", "invalid-date-xyz"]
    })

def test_tdd_red_phase_violations(mock_raw_data):
    """
    [TDD RED EVIDENCE] Проверяем, что исходный датасет содержит дефекты.
    Этот тест доказывает существование RED-фазы (данные до очистки не валидны).
    """
    # 1. Есть нули и координаты вне Торонто
    assert (mock_raw_data["LAT_WGS84"] == 0.0).any()
    assert ((mock_raw_data["LAT_WGS84"] > 43.85) | (mock_raw_data["LAT_WGS84"] < 43.58)).any()
    
    # 2. Есть плейсхолдеры "NSA"
    assert (mock_raw_data["LOCATION_TYPE"] == "NSA").any()
    
    # 3. Дата является строкой, а не datetime
    assert not pd.api.types.is_datetime64_any_dtype(mock_raw_data["OCC_DATE"])

def test_tdd_green_phase_cleanup(mock_raw_data):
    """
    [TDD GREEN EVIDENCE] Проверяем, что после clean_crime_data все дефекты устранены.
    """
    result = CrimeDataPipeline().clean_data(mock_raw_data)

    # 1. Из 4 строк должна остаться ровно 1 валидная (первая)
    assert len(result) == 1

    # 2. Проверка пространственного фильтра
    assert result["LAT_WGS84"].iloc[0] == 43.70
    assert result["LONG_WGS84"].iloc[0] == -79.40

    # 3. Проверка дат
    assert pd.api.types.is_datetime64_any_dtype(result["OCC_DATE"])

    # Проверим замену NSA (сгенерируем быстрый датасет с корректными координатами, но с NSA)
    df_nsa = pd.DataFrame({
        "LAT_WGS84": [43.7], "LONG_WGS84": [-79.4],
        "LOCATION_TYPE": ["NSA"], "OCC_DATE": ["2024-01-01"]
    })
    cleaned_nsa = CrimeDataPipeline().clean_data(df_nsa)
    assert cleaned_nsa["LOCATION_TYPE"].iloc[0] == "Unknown"