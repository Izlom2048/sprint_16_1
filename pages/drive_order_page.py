from __future__ import annotations

from data import LONG_TIMEOUT
from locators.drive_order_page_locators import DriveOrderPageLocators
from pages.base_page import BasePage


class DriveOrderPage(BasePage):
    def wait_for_drive_form(self) -> None:
        self.wait_for_visible(DriveOrderPageLocators.DRIVE_PREVIEW, timeout=LONG_TIMEOUT)
        self.wait_for_visible(DriveOrderPageLocators.RIGHTS_BUTTON, timeout=LONG_TIMEOUT)
