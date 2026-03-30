import allure


@allure.epic("Яндекс.Маршруты")
@allure.feature("Отрисовка маршрута")
class TestRouteRendering:
    @allure.title("При вводе двух разных адресов на карте отображаются точки маршрута")
    def test_route_points_render_for_two_preset_addresses(self, prepared_route):
        assert prepared_route.is_route_block_displayed(), "Блок маршрута не появился"
        assert prepared_route.has_route_polyline(), "Линия маршрута не отрисовалась"
        assert prepared_route.get_route_points_count() >= 2, "На карте меньше двух точек маршрута"
