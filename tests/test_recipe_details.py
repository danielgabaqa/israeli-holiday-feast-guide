from playwright.sync_api import expect

from pages.holiday_feast_page import HolidayFeastPage


def test_recipe_card_opens_complete_scaled_recipe(holiday_page: HolidayFeastPage) -> None:
    app = holiday_page
    app.select_holiday("tu-bav")
    app.select_category("desserts")

    app.open_recipe("tu-bav-desserts")
    expect(app.by_test_id("recipe-detail-title")).to_contain_text("Strawberry & cream tartlet")
    expect(app.by_test_id("recipe-detail-ingredients").get_by_test_id("detail-ingredient-quantity").first).to_have_text("200 g")
    expect(app.by_test_id("recipe-method").locator("li")).to_have_count(4)

    app.close_recipe()
    app.set_guest_count(10)
    app.open_recipe("tu-bav-desserts")
    expect(app.by_test_id("recipe-detail-ingredients").get_by_test_id("detail-ingredient-quantity").first).to_have_text("1000 g")
    app.close_recipe()
    app.by_test_id("mode-switch").check()
    dialog = app.open_recipe("tu-bav-desserts")
    expect(app.by_test_id("recipe-detail-ingredients").get_by_test_id("detail-ingredient-quantity").first).to_have_text("1200 g")
    expect(dialog).to_contain_text("Serves: 10")

    app.close_recipe()
