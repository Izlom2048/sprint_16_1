from __future__ import annotations

import re

import allure
from selenium.webdriver.common.by import By

from data import LONG_TIMEOUT
from locators.taxi_order_page_locators import TaxiOrderPageLocators
from pages.base_page import BasePage
from pages.phone_modal_page import PhoneModalPage


class TaxiOrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._current_tariff_name: str | None = None

    def wait_for_taxi_form(self) -> None:
        self.wait_for_visible(TaxiOrderPageLocators.TARIFF_PICKER, timeout=LONG_TIMEOUT)
        self.wait_for_visible(TaxiOrderPageLocators.SMART_ORDER_BUTTON, timeout=LONG_TIMEOUT)

    def get_tariffs_count(self) -> int:
        return len(self.find_all(TaxiOrderPageLocators.TARIFF_CARDS))

    def get_active_tariff_count(self) -> int:
        return len(self.find_all(TaxiOrderPageLocators.ACTIVE_TARIFF_CARD))

    def get_active_tariff_price(self) -> int:
        active_card = self.find_visible(TaxiOrderPageLocators.ACTIVE_TARIFF_CARD)
        price_text = active_card.find_element(By.CSS_SELECTOR, ".tcard-price").text.strip()
        return self.get_numeric_value(price_text)

    @allure.step("Выбрать тариф такси: {tariff_name}")
    def select_tariff(self, tariff_name: str) -> None:
        self.click(TaxiOrderPageLocators.tariff_card_by_name(tariff_name))
        self.wait_for_visible(TaxiOrderPageLocators.ACTIVE_TARIFF_CARD)

    def _get_tariff_card(self, tariff_name: str):
        return self.wait_for_presence(
            TaxiOrderPageLocators.tariff_card_by_name(tariff_name),
            timeout=LONG_TIMEOUT,
        )

    def _get_current_tooltip_root(self):
        if not self._current_tariff_name:
            raise AssertionError("Сначала вызови hover_over_tariff_info().")

        card = self._get_tariff_card(self._current_tariff_name)
        return card.find_element(By.CSS_SELECTOR, "[data-id='tooltip']")

    @allure.step("Навести курсор на подсказку тарифа: {tariff_name}")
    def hover_over_tariff_info(self, tariff_name: str) -> None:
        # На стенде tooltip уже лежит в DOM внутри карточки тарифа,
        # поэтому надёжнее читать его прямо из карточки, а не ждать реальный hover.
        self._current_tariff_name = tariff_name
        card = self._get_tariff_card(tariff_name)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            card,
        )
        card.find_element(By.CSS_SELECTOR, "[data-id='tooltip']")

    def _get_element_text_content(self, root, css_selector: str) -> str:
        elements = root.find_elements(By.CSS_SELECTOR, css_selector)
        if not elements:
            return ""

        return self.driver.execute_script(
            "return (arguments[0].textContent || '').trim();",
            elements[0],
        )

    def get_visible_tooltip_text(self) -> str:
        tooltip_root = self._get_current_tooltip_root()

        title = self._get_element_text_content(tooltip_root, ".i-title")
        prefix = self._get_element_text_content(tooltip_root, ".i-dPrefix")
        postfix = self._get_element_text_content(tooltip_root, ".i-dPostfix")

        return " ".join(part for part in [title, prefix, postfix] if part)

    def get_visible_tooltip_description(self) -> str:
        tooltip_root = self._get_current_tooltip_root()
        return self._get_element_text_content(tooltip_root, ".i-dPrefix")

    def has_phone_field(self) -> bool:
        return self.is_visible(TaxiOrderPageLocators.PHONE_BUTTON)

    def has_payment_field(self) -> bool:
        return self.is_visible(TaxiOrderPageLocators.PAYMENT_BUTTON)

    def has_comment_field(self) -> bool:
        return self.is_visible(TaxiOrderPageLocators.COMMENT_INPUT)

    def has_requirements_block(self) -> bool:
        return self.is_visible(TaxiOrderPageLocators.REQUIREMENTS_BLOCK)

    def get_order_button_text(self) -> str:
        return self.get_text(TaxiOrderPageLocators.SMART_ORDER_BUTTON_MAIN)

    @allure.step("Заполнить комментарий водителю: {comment}")
    def fill_comment(self, comment: str) -> None:
        self.type(TaxiOrderPageLocators.COMMENT_INPUT, comment)

    @allure.step("Включить дополнительную опцию: {label}")
    def enable_requirement(self, label: str) -> None:
        checkbox = self.wait_for_presence(
            TaxiOrderPageLocators.requirement_switch_by_label(label),
            timeout=LONG_TIMEOUT,
        )
        self.driver.execute_script("arguments[0].click();", checkbox)

    @allure.step("Нажать кнопку оформления заказа")
    def click_order_button(self) -> None:
        self.click(TaxiOrderPageLocators.SMART_ORDER_BUTTON)

    def phone_modal(self) -> PhoneModalPage:
        return PhoneModalPage(self.driver)

    def is_search_order_opened(self) -> bool:
        return self.is_visible(TaxiOrderPageLocators.ORDER_HEADER_TITLE) and self.get_order_header_title() == "Поиск машины"

    def get_order_header_title(self) -> str:
        return self.get_text(TaxiOrderPageLocators.ORDER_HEADER_TITLE)

    def get_order_timer_text(self) -> str:
        return self.get_text(TaxiOrderPageLocators.ORDER_HEADER_TIME)

    def is_order_progress_visible(self) -> bool:
        return self.is_visible(TaxiOrderPageLocators.ORDER_PROGRESS)

    def get_order_detail_value(self, label: str) -> str:
        return self.get_text(TaxiOrderPageLocators.order_detail_value_by_label(label))

    def get_driver_name(self) -> str:
        first_group = self.find_all(TaxiOrderPageLocators.ORDER_BUTTON_GROUPS)[0]
        return first_group.text.splitlines()[-1].strip()

    def get_driver_rating(self) -> str:
        return self.get_text(TaxiOrderPageLocators.DRIVER_RATING)

    def get_order_number(self) -> str:
        return self.get_text(TaxiOrderPageLocators.ORDER_NUMBER)

    @allure.step("Дождаться окна поиска машины")
    def wait_for_search_order(self) -> None:
        self.wait_until_text_matches(
            TaxiOrderPageLocators.ORDER_HEADER_TITLE,
            r"^Поиск машины$",
            timeout=LONG_TIMEOUT,
        )
        self.wait_for_visible(TaxiOrderPageLocators.ORDER_HEADER_TIME)

    @allure.step("Дождаться окна завершённого заказа")
    def wait_for_completed_order(self) -> None:
        self.wait_until_text_matches(
            TaxiOrderPageLocators.ORDER_HEADER_TITLE,
            r"\d+\s*мин\.\s*и\s*приедет",
            timeout=LONG_TIMEOUT,
        )
        self.wait_for_visible(TaxiOrderPageLocators.ORDER_NUMBER)

    def is_completed_order_displayed(self) -> bool:
        header = self.get_order_header_title()
        return re.search(r"\d+\s*мин\.\s*и\s*приедет", header) is not None

    @allure.step("Открыть детали заказа")
    def open_details(self) -> None:
        self.click(TaxiOrderPageLocators.order_button_by_text("Детали"))
        self.wait_for_visible(TaxiOrderPageLocators.ORDER_DETAILS)

    @allure.step("Отменить заказ")
    def cancel_order(self) -> None:
        self.click(TaxiOrderPageLocators.order_button_by_text("Отменить"))

    def is_order_closed(self) -> bool:
        return not self.is_visible(TaxiOrderPageLocators.ORDER_HEADER_TITLE, timeout=3)
