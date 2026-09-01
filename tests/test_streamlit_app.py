from streamlit.testing.v1 import AppTest


def test_streamlit_app_starts():
    app = AppTest.from_file("app/main.py").run(timeout=30)

    assert app.title[0].value == "FinXum"
    assert app.sidebar.radio[0].value == "New Assessment"
    assert not app.exception
