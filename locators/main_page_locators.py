from selenium.webdriver.common.by import By


class MainPageLocators:
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")

    WORKFLOW_SUBCONTAINER = (By.CSS_SELECTOR, ".workflow-subcontainer")
    ROUTE_BLOCK = (By.CSS_SELECTOR, ".type-picker")

    ACTIVE_MODE = (By.CSS_SELECTOR, ".modes-container .mode.active")
    ACTIVE_TRANSPORT = (By.CSS_SELECTOR, ".types-container .type.active")
    TRANSPORT_TYPES = (By.CSS_SELECTOR, ".types-container .type")

    RESULT_TEXT = (By.CSS_SELECTOR, ".results-container .text")
    RESULT_DURATION = (By.CSS_SELECTOR, ".results-container .duration")
    PRIMARY_ACTION_BUTTON = (By.CSS_SELECTOR, ".results-container .button.round")

    ROUTE_POLYLINE = (By.CSS_SELECTOR, "#map canvas")
    ROUTE_POINTS = (
        By.CSS_SELECTOR,
        ".ymaps-2-1-79-routerPoints-pane .ymaps-2-1-79-route-pin",
    )

    @staticmethod
    def mode_by_text(text: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'modes-container')]//div[contains(@class,'mode') and normalize-space()='{text}']",
        )

    @staticmethod
    def transport_by_index(index: int):
        return (
            By.CSS_SELECTOR,
            f".types-container .type:nth-child({index})",
        )
