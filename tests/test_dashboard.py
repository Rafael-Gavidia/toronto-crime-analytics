from pathlib import Path


def test_app_exists():

    assert Path("app.py").exists()


def test_pages_folder_exists():

    assert Path("views").exists()


def test_overview_page_exists():

    assert Path("views/overview.py").exists()