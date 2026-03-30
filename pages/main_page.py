from __future__ import annotations

import re

import allure
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

from data import BASE_URL, CUSTOM_MODE, FAST_MODE, LONG_TIMEOUT, TRANSPORT_INDEXES
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    @allure.step("Открыть Яндекс.Маршруты")
    def open_main_page(self) -> None:
        self.open(BASE_URL)
        self.wait_for_visible(MainPageLocators.FROM_INPUT)
        self.wait_for_visible(MainPageLocators.TO_INPUT)

    @allure.step("Заполнить маршрут: {from_address} -> {to_address}")
    def fill_route(self, from_address: str, to_address: str) -> None:
        self.type(MainPageLocators.FROM_INPUT, from_address)
        self.type(MainPageLocators.TO_INPUT, to_address)
        self.wait_for_route_results()

    @allure.step("Дождаться расчёта маршрута")
    def wait_for_route_results(self) -> None:
        self.wait_for_visible(MainPageLocators.ROUTE_BLOCK, timeout=LONG_TIMEOUT)
        self.wait_for_visible(MainPageLocators.RESULT_TEXT, timeout=LONG_TIMEOUT)
        self.wait_for_visible(MainPageLocators.RESULT_DURATION, timeout=LONG_TIMEOUT)

    def _safe_click(self, locator) -> None:
        element = self.wait_for_presence(locator, timeout=LONG_TIMEOUT)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )

        try:
            self.wait_for_clickable(locator, timeout=LONG_TIMEOUT).click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            element = self.wait_for_presence(locator, timeout=LONG_TIMEOUT)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Выбрать режим маршрута: {mode_name}")
    def select_mode(self, mode_name: str) -> None:
        self.wait_for_presence(MainPageLocators.WORKFLOW_SUBCONTAINER, timeout=LONG_TIMEOUT)
        self.wait_for_presence(MainPageLocators.ROUTE_BLOCK, timeout=LONG_TIMEOUT)

        self._safe_click(MainPageLocators.mode_by_text(mode_name))

        self.wait_until_text_matches(
            MainPageLocators.ACTIVE_MODE,
            rf"^{re.escape(mode_name)}$",
            timeout=LONG_TIMEOUT,
        )
        self.wait_for_route_results()

    def get_active_mode(self) -> str:
        return self.get_text(MainPageLocators.ACTIVE_MODE)

    @allure.step("Выбрать тип передвижения: {transport_name}")
    def select_transport(self, transport_name: str) -> None:
        index = TRANSPORT_INDEXES[transport_name]

        self.wait_for_presence(MainPageLocators.ROUTE_BLOCK, timeout=LONG_TIMEOUT)
        self._safe_click(MainPageLocators.transport_by_index(index))

        self.wait_for_presence(MainPageLocators.ACTIVE_TRANSPORT, timeout=LONG_TIMEOUT)
        self.wait_for_route_results()

    def are_custom_transport_types_enabled(self) -> bool:
        types = self.find_all(MainPageLocators.TRANSPORT_TYPES)
        return all("disabled" not in (element.get_attribute("class") or "") for element in types)

    def get_result_text(self) -> str:
        return self.get_text(MainPageLocators.RESULT_TEXT)

    def get_result_duration(self) -> str:
        return self.get_text(MainPageLocators.RESULT_DURATION)

    def get_result_summary(self) -> tuple[str, str]:
        return self.get_result_text(), self.get_result_duration()

    def is_route_block_displayed(self) -> bool:
        return self.is_visible(MainPageLocators.ROUTE_BLOCK)

    def is_primary_action_button_enabled(self) -> bool:
        return self.is_clickable(MainPageLocators.PRIMARY_ACTION_BUTTON)

    def get_primary_action_button_text(self) -> str:
        return self.get_text(MainPageLocators.PRIMARY_ACTION_BUTTON)

    @allure.step("Нажать основную кнопку действия")
    def click_primary_action(self) -> None:
        self._safe_click(MainPageLocators.PRIMARY_ACTION_BUTTON)

    def get_route_points_count(self) -> int:
        return len(self.find_all(MainPageLocators.ROUTE_POINTS))

    def has_route_polyline(self) -> bool:
        return self.is_visible(MainPageLocators.ROUTE_POLYLINE)

    def get_same_address_summary(self) -> str:
        self.wait_for_route_results()
        return f"{self.get_result_text()} {self.get_result_duration()}"

    @allure.step("Подготовить маршрут для такси")
    def prepare_fast_taxi_route(self, from_address: str, to_address: str) -> None:
        self.fill_route(from_address, to_address)
        if self.get_active_mode() != FAST_MODE:
            self.select_mode(FAST_MODE)

    @allure.step("Подготовить маршрут для Драйва")
    def prepare_drive_route(self, from_address: str, to_address: str) -> None:
        self.fill_route(from_address, to_address)
        if self.get_active_mode() != CUSTOM_MODE:
            self.select_mode(CUSTOM_MODE)
        self.select_transport("Драйв")