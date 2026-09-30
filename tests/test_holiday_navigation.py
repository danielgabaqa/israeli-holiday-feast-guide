import pytest
from playwright.sync_api import expect

from pages.holiday_feast_page import HolidayFeastPage

HOLIDAYS = [
    "yom-haatzmaut",
    "tu-bav",
    "rosh-hashanah",
    "sukkot",
    "hanukkah",
    "purim",
    "pesach",
    "shavuot",
    "tu-bishvat",
]
CATEGORIES = ["starters", "mains", "desserts", "drinks"]


@pytest.mark.parametrize("holiday_id", HOLIDAYS)
def test_each_holiday_has_recipes_for_each_category(
    holiday_page: HolidayFeastPage, holiday_id: str
) -> None:
    app = holiday_page
    app.select_holiday(holiday_id)
    expect(app.by_test_id("holiday-heading")).not_to_be_empty()
    fit_count = app.recipe_cards.count()
    assert fit_count > 0

    app.by_test_id("mode-switch").check()
    feast_count = app.recipe_cards.count()
    assert feast_count > fit_count

    for category_id in CATEGORIES:
        app.select_category(category_id)
        assert app.recipe_cards.count() > 0
        expect(app.recipe_cards.first.get_by_test_id("recipe-title")).not_to_be_empty()
        expect(app.recipe_cards.first.get_by_test_id("recipe-calories")).to_contain_text("kcal")


def test_recipe_layout_adapts_to_mobile_width(holiday_page: HolidayFeastPage) -> None:
    page = holiday_page.page
    page.set_viewport_size({"width": 390, "height": 844})

    expect(holiday_page.by_test_id("header-title")).to_be_visible()
    expect(holiday_page.recipe_cards).not_to_have_count(0)
    layout = page.evaluate("""() => ({
            viewportWidth: document.documentElement.clientWidth,
            contentWidth: document.documentElement.scrollWidth,
            recipeColumns: getComputedStyle(document.querySelector('.recipe-grid')).gridTemplateColumns.split(' ').length
        })""")
    assert layout["contentWidth"] <= layout["viewportWidth"]
    assert layout["recipeColumns"] == 1
