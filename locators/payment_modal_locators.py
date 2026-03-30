from selenium.webdriver.common.by import By


class PaymentModalLocators:
    MODAL = (By.CSS_SELECTOR, ".payment-picker .modal")

    @staticmethod
    def payment_row_by_title(title: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'payment-picker')]//div[contains(@class,'pp-row')][.//div[contains(@class,'pp-title') and normalize-space()='{title}']]",
        )
