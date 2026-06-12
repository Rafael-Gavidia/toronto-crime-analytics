from pathlib import Path


def test_app_exists():

    assert Path("app.py").exists()


def test_pages_folder_exists():

    assert Path("pages").exists()


def test_overview_page_exists():

    assert Path("pages/overview.py").exists()