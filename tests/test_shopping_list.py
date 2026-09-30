from playwright.sync_api import expect

from pages.holiday_feast_page import HolidayFeastPage


def test_shopping_list_contains_scaled_items_and_checkoff(holiday_page: HolidayFeastPage) -> None:
    app = holiday_page
    app.select_holiday("tu-bav")
    app.by_test_id("mode-switch").check()
    app.add_recipe_to_shopping_list("tu-bav-drinks-2")
    app.select_category("desserts")
    app.add_recipe_to_shopping_list("tu-bav-desserts")

    app.set_guest_count(10)
    drawer = app.open_shopping_list()
    expect(drawer).to_contain_text("2 recipes")
    expect(drawer).to_contain_text("1200 g")
    expect(drawer).to_contain_text("1440 ml")
    expect(drawer).to_contain_text("Strawberry & cream tartlet")
    expect(drawer).to_contain_text("Pomegranate-cranberry sparkler")

    flour_item = app.shopping_item("flour")
    expect(flour_item).to_have_count(1)
    flour_item.locator("input").check()
    expect(flour_item.locator("input")).to_be_checked()
    expect(flour_item).to_have_class("shopping-item checked")


def test_matching_ingredients_are_combined_across_recipes(holiday_page: HolidayFeastPage) -> None:
    app = holiday_page
    app.add_recipe_to_shopping_list("yom-haatzmaut-starters")
    app.add_recipe_to_shopping_list("yom-haatzmaut-mains")

    drawer = app.open_shopping_list()
    olive_oil = drawer.locator(".shopping-item").filter(has_text="olive oil")
    expect(olive_oil).to_have_count(1)
    expect(olive_oil).to_contain_text("45 ml")
    expect(olive_oil).to_contain_text("Israeli-style chicken & beef parghiot skewers")
