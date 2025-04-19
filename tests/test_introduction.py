import streamlit as st
from streamlit.runtime.scriptrunner import RerunException


def test_introduction_page(monkeypatch):
    """Test that the introduction page renders without errors."""
    # Mock Streamlit functions to prevent actual rendering
    monkeypatch.setattr(st, "markdown", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "header", lambda *args, **kwargs: None)

    # Import the introduction page
    try:
        import src.pages.introduction
    except RerunException:
        # Ignore rerun exceptions triggered by Streamlit
        pass

    # If no exceptions are raised, the test passes
    assert True
