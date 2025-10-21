import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service


@pytest.fixture
def dash_duo(request):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')

    # Path to msedgedriver.exe (update path to where you saved it)
    service = Service('msedgedriver.exe')

    driver = webdriver.Edge(service=service, options=options)
    yield driver
    driver.quit()