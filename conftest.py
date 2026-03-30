from __future__ import annotations

import os

import pytest
from selenium import webdriver

from data import FROM_ADDRESS, TO_ADDRESS
from pages.drive_order_page import DriveOrderPage
from pages.main_page import MainPage
from pages.taxi_order_page import TaxiOrderPage


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=ru-RU")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


@pytest.fixture
def main_page(driver) -> MainPage:
    page = MainPage(driver)
    page.open_main_page()
    return page


@pytest.fixture
def prepared_route(main_page: MainPage) -> MainPage:
    main_page.fill_route(FROM_ADDRESS, TO_ADDRESS)
    return main_page


@pytest.fixture
def prepared_fast_route(main_page: MainPage) -> MainPage:
    main_page.prepare_fast_taxi_route(FROM_ADDRESS, TO_ADDRESS)
    return main_page


@pytest.fixture
def taxi_order_page(prepared_fast_route: MainPage) -> TaxiOrderPage:
    prepared_fast_route.click_primary_action()
    page = TaxiOrderPage(prepared_fast_route.driver)
    page.wait_for_taxi_form()
    return page


@pytest.fixture
def drive_order_page(main_page: MainPage) -> DriveOrderPage:
    main_page.prepare_drive_route(FROM_ADDRESS, TO_ADDRESS)
    page = DriveOrderPage(main_page.driver)
    page.wait_for_drive_form()
    return page
