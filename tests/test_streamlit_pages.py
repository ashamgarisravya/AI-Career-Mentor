from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


@pytest.mark.integration
def test_streamlit_pages_load_without_exceptions() -> None:
    files = [Path("app.py"), *sorted(Path("pages").glob("*.py"))]
    failures: list[str] = []

    for path in files:
        app = AppTest.from_file(str(path), default_timeout=25)
        app.run()
        if app.exception:
            messages = ", ".join(str(exception.value) for exception in app.exception)
            failures.append(f"{path}: {messages}")

    assert not failures, "\n".join(failures)
