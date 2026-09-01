from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app" / "main.py"


def test_streamlit_app_starts():
    app = AppTest.from_file(APP_PATH).run(timeout=30)

    assert app.title[0].value == "FinXum"
    assert app.sidebar.radio[0].value == "New Assessment"
    assert not app.exception
