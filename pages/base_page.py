from playwright.sync_api import Page, expect


class BasePage:
    """Shared browser actions and stable test-id access for app pages."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/index.html") -> None:
        self.page.goto(f"{self.base_url}{path}", wait_until="domcontentloaded")

    def by_test_id(self, test_id: str):
        return self.page.get_by_test_id(test_id)

    def wait_for(self, test_id: str):
        locator = self.by_test_id(test_id)
        expect(locator).to_be_visible()
        return locator
