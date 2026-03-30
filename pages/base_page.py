from __future__ import annotations

import re
from typing import Tuple

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data import DEFAULT_TIMEOUT

Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.short_wait = WebDriverWait(driver, 3)

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str) -> None:
        self.driver.get(url)

    def wait_for_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Locator, timeout: int | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, locator: Locator, timeout: int | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_invisible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait_for_visible(locator)

    def find_all(self, locator: Locator) -> list[WebElement]:
        self.wait_for_presence(locator)
        return self.driver.find_elements(*locator)

    @allure.step("Клик по элементу")
    def click(self, locator: Locator) -> None:
        self.wait_for_clickable(locator).click()

    @allure.step("Ввести текст: {text}")
    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.wait_for_visible(locator)
        if clear:
            self.clear(locator)
        element.send_keys(text)

    @allure.step("Очистить поле")
    def clear(self, locator: Locator) -> None:
        element = self.wait_for_visible(locator)
        element.clear()
        self.driver.execute_script("arguments[0].value = '';", element)

    def get_text(self, locator: Locator) -> str:
        return self.wait_for_visible(locator).text.strip()

    def is_visible(self, locator: Locator, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_clickable(self, locator: Locator, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def wait_until_text_matches(self, locator: Locator, pattern: str, timeout: int) -> str:
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: re.search(pattern, d.find_element(*locator).text.strip()) is not None)
        return self.get_text(locator)

    def get_numeric_value(self, text: str) -> int:
        numbers = re.findall(r"\d+", text.replace(" ", ""))
        if not numbers:
            raise AssertionError(f"Не удалось извлечь число из строки: {text}")
        return int(numbers[0])
