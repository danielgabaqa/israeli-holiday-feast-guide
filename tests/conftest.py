from __future__ import annotations

import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest
from playwright.sync_api import Browser

from pages.holiday_feast_page import HolidayFeastPage

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _free_port() -> int:
    with socket.socket() as server_socket:
        server_socket.bind(("127.0.0.1", 0))
        return int(server_socket.getsockname()[1])


@pytest.fixture(scope="session")
def app_url() -> Iterator[str]:
    """Serve the standalone HTML app over HTTP for the duration of the test run."""
    port = _free_port()
    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(50):
            if process.poll() is not None:
                raise RuntimeError("The local app server exited before becoming ready.")
            try:
                with urllib.request.urlopen(f"{url}/index.html", timeout=0.5) as response:
                    if response.status == 200:
                        break
            except (urllib.error.URLError, TimeoutError):
                time.sleep(0.1)
        else:
            raise RuntimeError("The local app server did not become ready within five seconds.")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)


@pytest.fixture
def holiday_page(browser: Browser, app_url: str) -> Iterator[HolidayFeastPage]:
    """Provide a clean browser context so localStorage cannot leak between tests."""
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, locale="en-US")
    page = context.new_page()
    app = HolidayFeastPage(page, app_url)
    app.open()
    yield app
    context.close()
