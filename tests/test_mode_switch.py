import re

from playwright.sync_api import expect

from pages.holiday_feast_page import HolidayFeastPage


def _calorie_value(text: str) -> int:
    match = re.search(r"(\d+)\s+kcal", text)
    assert match, f"Could not parse calories from {text!r}"
    return int(match.group(1))


def test_full_feast_mode_updates_calories_and_ingredient_quantities(holiday_page: HolidayFeastPage) -> None:
    app = holiday_page
    mode_switch = app.by_test_id("mode-switch")
    card = app.recipe_cards.first
    fit_count = app.recipe_cards.count()
    calories_fit = _calorie_value(card.get_by_test_id("recipe-calories").inner_text())
    ingredients_fit = card.get_by_test_id("ingredient-quantity").all_inner_texts()

    expect(mode_switch).not_to_be_checked()
    assert calories_fit < 500
    expect(app.by_test_id("macro-summary")).to_contain_text("Per guest")

    mode_switch.check()
    expect(mode_switch).to_be_checked()
    assert app.recipe_cards.count() > fit_count
    calories_feast = _calorie_value(card.get_by_test_id("recipe-calories").inner_text())
    ingredients_feast = card.get_by_test_id("ingredient-quantity").all_inner_texts()

    assert calories_feast > calories_fit
    assert ingredients_feast != ingredients_fit
