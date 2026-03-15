import pytest
from app import app
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def flask_app():
    # Setup
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # Yield the testing app
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="class")
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless"
    )  # Run in background, remove to see browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def live_server(flask_app):
    # This would normally set up a live server, but for simplicity
    # we'll use the test client and navigate to routes
    return flask_app
