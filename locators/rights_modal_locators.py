from selenium.webdriver.common.by import By


class RightsModalLocators:
    MODAL = (By.CSS_SELECTOR, ".number-picker .modal")
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    BIRTH_DATE = (By.ID, "birthDate")
    NUMBER = (By.ID, "number")

    @staticmethod
    def button_by_text(text: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'number-picker')]//button[normalize-space()='{text}']",
        )

    @staticmethod
    def head_by_text(text: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'number-picker')]//div[contains(@class,'head') and normalize-space()='{text}']",
        )
