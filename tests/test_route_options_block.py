import allure

from data import FROM_ADDRESS, SAME_ADDRESS, ZERO_ROUTE_DURATION, ZERO_ROUTE_TEXT


@allure.epic("Яндекс.Маршруты")
@allure.feature("Блок выбора маршрута")
class TestRouteOptionsBlock:
    @allure.title("При вводе разных адресов отображается блок выбора маршрута")
    def test_route_block_displayed_for_different_addresses(self, prepared_route):
        assert prepared_route.is_route_block_displayed(), "Блок выбора маршрута не отобразился"

    @allure.title("При одинаковых адресах отображается нулевой маршрут")
    def test_same_addresses_show_free_zero_min_route(self, main_page):
        main_page.fill_route(FROM_ADDRESS, SAME_ADDRESS)
        result_text, result_duration = main_page.get_result_summary()

        assert result_text == ZERO_ROUTE_TEXT
        assert result_duration == ZERO_ROUTE_DURATION
