from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app" / "main.py"


def test_streamlit_app_starts():
    app = AppTest.from_file(APP_PATH).run(timeout=30)

    assert app.title[0].value == "FinXum"
    assert app.sidebar.radio[0].value == "New Assessment"
    assert not app.exception


def test_analytics_page_is_navigable():
    app = AppTest.from_file(APP_PATH).run(timeout=30)

    app.sidebar.radio[0].set_value("Analytics").run(timeout=30)

    assert not app.exception
    assert app.header[0].value == "Analytics"


def test_load_synthetic_demo_button_populates_history_without_duplicates(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    app = AppTest.from_file(APP_PATH).run(timeout=30)
    app.sidebar.radio[0].set_value("Analytics").run(timeout=30)
    assert not app.exception

    app.button[0].click().run(timeout=30)
    assert not app.exception

    app.sidebar.radio[0].set_value("History").run(timeout=30)
    assert not app.exception
    assert len(app.dataframe) == 1
    assert len(app.dataframe[0].value) == 25

    app.sidebar.radio[0].set_value("Analytics").run(timeout=30)
    app.button[0].click().run(timeout=30)
    assert not app.exception

    app.sidebar.radio[0].set_value("History").run(timeout=30)
    assert len(app.dataframe[0].value) == 25


def test_new_assessment_form_is_rate_limited_per_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    app = AppTest.from_file(APP_PATH).run(timeout=30)
    assert not app.exception

    for _ in range(5):
        app.button[0].click().run(timeout=30)
        assert not app.exception
        assert app.success

    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert app.error
    assert "Too many assessments submitted" in app.error[0].value


def test_shows_persistence_warning_without_database_url(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    app = AppTest.from_file(APP_PATH).run(timeout=30)
    assert not app.exception
    assert any("non-persistent storage" in w.value for w in app.warning)
