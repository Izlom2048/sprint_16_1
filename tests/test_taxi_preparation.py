import allure
import pytest

from data import CUSTOM_MODE, FAST_MODE, FROM_ADDRESS, OPTIMAL_MODE, TO_ADDRESS


@allure.epic("Яндекс.Маршруты")
@allure.feature("Подготовка к заказу такси")
class TestTaxiPreparation:
    @pytest.mark.xfail(reason="На стенде пересчёт параметров между режимами иногда не происходит")
    @allure.title("При переключении между Оптимальным и Быстрым меняются активный таб и параметры маршрута")
    def test_switch_between_optimal_and_fast_recalculates_time_and_price(self, prepared_fast_route):
        fast_summary = prepared_fast_route.get_result_summary()
        assert prepared_fast_route.get_active_mode() == FAST_MODE

        prepared_fast_route.select_mode(OPTIMAL_MODE)
        optimal_summary = prepared_fast_route.get_result_summary()

        assert prepared_fast_route.get_active_mode() == OPTIMAL_MODE
        assert fast_summary != optimal_summary, "Стоимость и время не изменились при переключении режима"

    @allure.title("В режиме Свой становятся доступны типы передвижения")
    def test_custom_mode_enables_transport_types(self, prepared_route):
        prepared_route.select_mode(CUSTOM_MODE)
        assert prepared_route.get_active_mode() == CUSTOM_MODE
        assert prepared_route.are_custom_transport_types_enabled(), "Типы передвижения остались неактивными"

    @allure.title("В режиме Быстрый активна кнопка Вызвать такси")
    def test_fast_mode_has_call_taxi_button(self, prepared_fast_route):
        assert prepared_fast_route.get_active_mode() == FAST_MODE
        assert prepared_fast_route.get_primary_action_button_text() == "Вызвать такси"
        assert prepared_fast_route.is_primary_action_button_enabled()

    @allure.title("В режиме Свой для типа Драйв активна кнопка Забронировать")
    def test_drive_type_has_book_button(self, main_page):
        main_page.prepare_drive_route(FROM_ADDRESS, TO_ADDRESS)

        assert main_page.get_primary_action_button_text() == "Забронировать"
        assert main_page.is_primary_action_button_enabled(), "Кнопка 'Забронировать' не активна"
