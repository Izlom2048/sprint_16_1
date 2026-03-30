import allure
import pytest

from data import COMMENT, NOTEBOOK_TABLE, PHONE_NUMBER, SMS_CODE, TAXI_TARIFFS, WORK_TARIFF


TOOLTIP_CASES = [
    pytest.param(
        "Рабочий",
        TAXI_TARIFFS["Рабочий"],
        id="work",
    ),
    pytest.param(
        "Сонный",
        TAXI_TARIFFS["Сонный"],
        marks=pytest.mark.xfail(reason="На стенде у тарифа 'Сонный' отображается неверное описание"),
        id="sleepy",
    ),
    pytest.param(
        "Отпускной",
        TAXI_TARIFFS["Отпускной"],
        id="vacation",
    ),
    pytest.param(
        "Разговорчивый",
        TAXI_TARIFFS["Разговорчивый"],
        marks=pytest.mark.xfail(reason="На стенде у тарифа 'Разговорчивый' может показываться неверное описание"),
        id="talkative",
    ),
    pytest.param(
        "Утешительный",
        TAXI_TARIFFS["Утешительный"],
        id="comforting",
    ),
    pytest.param(
        "Глянцевый",
        TAXI_TARIFFS["Глянцевый"],
        id="glossy",
    ),
]


@allure.epic("Яндекс.Маршруты")
@allure.feature("Заказ тарифа Такси")
class TestTaxiOrder:
    @allure.title("Открывается форма заказа такси с шестью тарифами и одним активным")
    def test_taxi_form_has_six_tariffs_and_one_active(self, taxi_order_page):
        assert taxi_order_page.get_tariffs_count() == 6
        assert taxi_order_page.get_active_tariff_count() == 1

    @pytest.mark.parametrize("tariff_name, expected_description", TOOLTIP_CASES)
    @allure.title("Подсказка тарифа соответствует ТЗ")
    def test_taxi_tariff_tooltips_match_tz(self, taxi_order_page, tariff_name, expected_description):
        taxi_order_page.hover_over_tariff_info(tariff_name)

        tooltip_text = taxi_order_page.get_visible_tooltip_text()
        tooltip_description = taxi_order_page.get_visible_tooltip_description()

        assert tariff_name in tooltip_text, f"В подсказке не найдено название тарифа {tariff_name}"
        assert tooltip_description == expected_description, (
            f"Описание тарифа '{tariff_name}' не совпадает с ТЗ. "
            f"Ожидалось: '{expected_description}', получено: '{tooltip_description}'"
        )

    @allure.title("Под тарифами отображаются обязательные поля формы")
    def test_taxi_form_contains_required_fields(self, taxi_order_page):
        assert taxi_order_page.has_phone_field(), "Поле Телефон не отображается"
        assert taxi_order_page.has_payment_field(), "Поле Способ оплаты не отображается"
        assert taxi_order_page.has_comment_field(), "Поле Комментарий водителю не отображается"
        assert taxi_order_page.has_requirements_block(), "Блок Требования к заказу не отображается"
        assert taxi_order_page.get_order_button_text() == "Ввести номер и заказать"

    @pytest.mark.xfail(reason="На стенде после отмены заказа окно заказа не закрывается")
    @allure.title("Полный флоу заказа такси для тарифа Рабочий")
    def test_work_tariff_full_flow(self, taxi_order_page):
        taxi_order_page.select_tariff(WORK_TARIFF)
        selected_price = taxi_order_page.get_active_tariff_price()
        taxi_order_page.enable_requirement(NOTEBOOK_TABLE)
        taxi_order_page.fill_comment(COMMENT)
        taxi_order_page.click_order_button()

        phone_modal = taxi_order_page.phone_modal()
        if phone_modal.is_opened():
            phone_modal.fill_phone(PHONE_NUMBER)
            phone_modal.confirm_sms_code(SMS_CODE)

        taxi_order_page.wait_for_search_order()

        assert taxi_order_page.get_order_header_title() == "Поиск машины"
        assert taxi_order_page.get_order_timer_text(), "Таймер поиска не отображается"
        assert taxi_order_page.is_order_progress_visible(), "Прогресс поиска не отображается"

        taxi_order_page.wait_for_completed_order()

        assert taxi_order_page.is_completed_order_displayed(), "Окно совершённого заказа не появилось"
        assert taxi_order_page.get_order_number(), "Номер автомобиля не отображается"
        assert taxi_order_page.get_driver_name(), "Имя водителя не отображается"
        assert taxi_order_page.get_driver_rating(), "Рейтинг водителя не отображается"

        taxi_order_page.open_details()
        detail_price_text = taxi_order_page.get_order_detail_value("Еще про поездку")
        assert taxi_order_page.get_numeric_value(detail_price_text) == selected_price

        taxi_order_page.cancel_order()
        assert taxi_order_page.is_order_closed(), "Окно заказа не закрылось после отмены"