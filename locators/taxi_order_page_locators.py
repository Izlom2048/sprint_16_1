from selenium.webdriver.common.by import By


class TaxiOrderPageLocators:
    TARIFF_PICKER = (By.CSS_SELECTOR, ".tariff-picker.shown")
    TARIFF_CARDS = (By.CSS_SELECTOR, ".tariff-cards .tcard")
    ACTIVE_TARIFF_CARD = (By.CSS_SELECTOR, ".tariff-cards .tcard.active")

    PHONE_BUTTON = (By.CSS_SELECTOR, ".form .np-button")
    PAYMENT_BUTTON = (By.CSS_SELECTOR, ".form .pp-button")
    COMMENT_INPUT = (By.ID, "comment")
    REQUIREMENTS_BLOCK = (By.CSS_SELECTOR, ".form .reqs")
    SMART_ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button")
    SMART_ORDER_BUTTON_MAIN = (By.CSS_SELECTOR, ".smart-button-main")

    ORDER_HEADER_TITLE = (By.CSS_SELECTOR, ".order .order-header-title")
    ORDER_HEADER_TIME = (By.CSS_SELECTOR, ".order .order-header-time")
    ORDER_PROGRESS = (By.CSS_SELECTOR, ".order .order-progress")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order .order-number .number")
    DRIVER_RATING = (By.CSS_SELECTOR, ".order .order-btn-rating")
    ORDER_DETAILS = (By.CSS_SELECTOR, ".order .order-details")
    ORDER_BUTTON_GROUPS = (By.CSS_SELECTOR, ".order .order-btn-group")

    @staticmethod
    def tariff_card_by_name(name: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'tcard')][.//div[contains(@class,'tcard-title') and normalize-space()='{name}']]",
        )

    @staticmethod
    def requirement_switch_by_label(label: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'r-sw-container')][.//div[contains(@class,'r-sw-label') and normalize-space()='{label}']]//input[@type='checkbox']",
        )

    @staticmethod
    def order_button_by_text(text: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'order-btn-group')][.//div[normalize-space()='{text}']]//button",
        )

    @staticmethod
    def order_detail_value_by_label(label: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'order-details-row')][.//div[contains(@class,'o-d-h') and normalize-space()='{label}']]//div[contains(@class,'o-d-sh')]",
        )