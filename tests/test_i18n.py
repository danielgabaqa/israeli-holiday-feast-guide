from playwright.sync_api import expect

from pages.holiday_feast_page import HolidayFeastPage


def test_language_toggle_updates_direction_layout_and_persists(holiday_page: HolidayFeastPage) -> None:
    page = holiday_page.page
    toggle = holiday_page.by_test_id("lang-toggle")

    expect(page.locator("html")).to_have_attribute("lang", "en")
    expect(page.locator("html")).to_have_attribute("dir", "ltr")
    expect(holiday_page.by_test_id("header-title")).to_contain_text("Gather around")

    toggle.click()
    expect(page.locator("html")).to_have_attribute("lang", "he")
    expect(page.locator("html")).to_have_attribute("dir", "rtl")
    expect(holiday_page.by_test_id("header-title")).to_contain_text("מתכנסים")
    assert page.locator(".holiday-nav").evaluate("element => getComputedStyle(element).direction") == "rtl"

    toggle.click()
    expect(page.locator("html")).to_have_attribute("dir", "ltr")
    expect(holiday_page.by_test_id("header-title")).to_contain_text("Gather around")

    page.reload()
    expect(page.locator("html")).to_have_attribute("lang", "en")
    expect(page.locator("html")).to_have_attribute("dir", "ltr")
