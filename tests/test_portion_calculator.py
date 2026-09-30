from playwright.sync_api import expect

from pages.holiday_feast_page import HolidayFeastPage


def test_tu_bav_flour_and_macros_scale_with_guest_count(holiday_page: HolidayFeastPage) -> None:
    app = holiday_page
    app.select_holiday("tu-bav")
    app.select_category("desserts")
    tartlet = app.recipe_card("tu-bav-desserts")

    expect(tartlet.get_by_test_id("recipe-title")).to_contain_text("Strawberry & cream tartlet")
    expect(tartlet.get_by_test_id("ingredient-quantity").first).to_have_text("200 g")

    app.set_guest_count(10)
    expect(tartlet.get_by_test_id("ingredient-quantity").first).to_have_text("1000 g")
    expect(app.by_test_id("macro-summary")).to_contain_text("Protein: 50g")
    expect(app.by_test_id("macro-summary")).to_contain_text("Total for 10: 2920 kcal")


def test_guest_count_boundaries_and_stepper_clamping(holiday_page: HolidayFeastPage) -> None:
    app = holiday_page
    app.set_guest_count(1)
    expect(app.guest_input).to_have_value("1")
    expect(app.recipe_cards.first.get_by_test_id("ingredient-quantity").first).to_have_text("120 g")
    app.decrement_guests()
    expect(app.guest_input).to_have_value("1")

    app.set_guest_count(20)
    expect(app.guest_input).to_have_value("20")
    expect(app.recipe_cards.first.get_by_test_id("ingredient-quantity").first).to_have_text("2400 g")
    app.increment_guests()
    expect(app.guest_input).to_have_value("20")
