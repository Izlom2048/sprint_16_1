from selenium.webdriver.common.by import By


class DriveOrderPageLocators:
    DRIVE_PREVIEW = (By.CSS_SELECTOR, ".drive-preview")
    RIGHTS_BUTTON = (By.CSS_SELECTOR, ".form .np-button")
    RIGHTS_BUTTON_TEXT = (By.CSS_SELECTOR, ".form .np-button .np-text")
    PAYMENT_BUTTON = (By.CSS_SELECTOR, ".form .pp-button")
    REQUIREMENTS_HEADER = (By.CSS_SELECTOR, ".form .reqs .reqs-head")
