from selenium.webdriver.common.by import By


class PhoneModalLocators:
    MODAL = (By.CSS_SELECTOR, ".number-picker .modal")
    PHONE_INPUT = (By.ID, "phone")
    CODE_INPUT = (By.ID, "code")

    @staticmethod
    def button_by_text(text: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'number-picker')]//button[normalize-space()='{text}']",
        )
