from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class HolidayFeastPage(BasePage):
    """Page object for the holiday selector, recipe cards, and shopping drawer."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    @property
    def recipe_cards(self) -> Locator:
        return self.by_test_id("recipe-card")

    @property
    def guest_input(self) -> Locator:
        return self.by_test_id("guest-counter-input")

    def select_holiday(self, holiday_id: str) -> None:
        tab = self.by_test_id(f"holiday-tab-{holiday_id}")
        tab.click()
        expect(tab).to_have_attribute("aria-selected", "true")

    def select_category(self, category_id: str) -> None:
        button = self.by_test_id(f"category-filter-{category_id}")
        button.click()
        expect(button).to_have_attribute("aria-pressed", "true")

    def recipe_card(self, recipe_id: str) -> Locator:
        return self.page.locator(f'[data-testid="recipe-card"][data-recipe-id="{recipe_id}"]')

    def open_recipe(self, recipe_id: str) -> Locator:
        self.recipe_card(recipe_id).get_by_test_id("open-recipe").click()
        dialog = self.by_test_id("recipe-dialog")
        expect(dialog).to_be_visible()
        return dialog

    def close_recipe(self) -> None:
        self.by_test_id("recipe-dialog-close").click()
        expect(self.by_test_id("recipe-dialog")).not_to_be_visible()

    def set_guest_count(self, count: int) -> None:
        self.guest_input.fill(str(count))
        self.guest_input.dispatch_event("change")
        expect(self.guest_input).to_have_value(str(count))

    def increment_guests(self, amount: int = 1) -> None:
        for _ in range(amount):
            self.by_test_id("guest-increment").click()

    def decrement_guests(self, amount: int = 1) -> None:
        for _ in range(amount):
            self.by_test_id("guest-decrement").click()

    def add_recipe_to_shopping_list(self, recipe_id: str) -> None:
        checkbox = self.recipe_card(recipe_id).get_by_test_id("add-to-shopping-list")
        checkbox.check()
        expect(checkbox).to_be_checked()

    def open_shopping_list(self) -> Locator:
        self.by_test_id("shopping-list-btn").click()
        drawer = self.by_test_id("shopping-list-drawer")
        expect(drawer).to_be_visible()
        return drawer

    def shopping_item(self, ingredient_name: str) -> Locator:
        return self.page.locator(".shopping-item").filter(has_text=ingredient_name)
