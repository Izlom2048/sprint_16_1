from __future__ import annotations

import allure

from locators.phone_modal_locators import PhoneModalLocators
from pages.base_page import BasePage


class PhoneModalPage(BasePage):
    def is_opened(self) -> bool:
        return self.is_visible(PhoneModalLocators.MODAL)

    @allure.step("Заполнить телефон: {phone_number}")
    def fill_phone(self, phone_number: str) -> None:
        self.type(PhoneModalLocators.PHONE_INPUT, phone_number)
        self.click(PhoneModalLocators.button_by_text("Далее"))

    @allure.step("Подтвердить код из СМС: {code}")
    def confirm_sms_code(self, code: str) -> None:
        self.wait_for_visible(PhoneModalLocators.CODE_INPUT)
        self.type(PhoneModalLocators.CODE_INPUT, code)
        self.click(PhoneModalLocators.button_by_text("Подтвердить"))
