# The Holy Day Table

Israeli Holiday Feast Guide, with recipes and celebrations across the Hebrew calendar.

This portfolio project combines an Israeli holiday recipe guide with browser automation examples using Python and Playwright. The app is a standalone `index.html`; the E2E suite serves it locally and exercises it in a real browser.

## Features

- Switch between English and Hebrew; the document language, text direction, and RTL layout update together.
- Browse recipes for nine holidays: Yom Ha'atzmaut, Tu B'Av, Rosh Hashanah, Sukkot, Hanukkah, Purim, Pesach, Shavuot, and Tu BiShvat.
- Filter recipes by category: starters, mains, desserts, and drinks.
- Search by dish name, description, ingredient, or holiday, with a live result count.
- Open recipe details with ingredients, serving adjustments, cooking times, nutrition estimates, and method steps.
- Switch from Fit & Festive to Full Feast, which adds recipes without changing the ingredients or values of recipes already shown.
- Build a meal plan and use cooking mode with saved step completion and a countdown timer.
- Scale ingredient quantities and nutrition totals for 1 to 20 guests.
- Create an interactive shopping list grouped by recipe.

Calories and macronutrients are illustrative portfolio data, not medical or dietary advice.

## Application Architecture

`index.html` contains the semantic markup, CSS, and JavaScript. Holiday, translation, and recipe data are defined in the script, while interface state is held in the `state` object. The `render()` function updates labels, tabs, filters, recipe cards, nutrition summaries, and shopping-list counts.

### Languages and RTL

The language toggle updates `document.documentElement.lang` and `dir`: English uses `lang="en" dir="ltr"`, and Hebrew uses `lang="he" dir="rtl"`. Logical CSS properties such as `margin-inline`, `inset-inline-end`, and `border-inline-start` let components adapt to either direction. The selected language is stored in `localStorage`; the i18n tests check document attributes and layout direction.

```js
document.documentElement.lang = state.lang;
document.documentElement.dir = state.lang === "he" ? "rtl" : "ltr";
localStorage.setItem("feast-language", state.lang);
```

### Menu Modes and Serving Adjustments

Full Feast adds holiday recipes to the regular menu without changing the portions of recipes already shown. Each recipe has its own illustrative calorie and macronutrient values. Guest count is the only ingredient multiplier:

```text
quantity = base quantity x guest count / 2
```

Calories are listed per serving; the summary multiplies them by the guest count. Protein, carbohydrates, and fat are totaled across the displayed recipes and scaled by the number of guests. For example, 200 g of flour for two guests becomes 1,000 g for ten guests in either menu mode.

### Shopping List and Meal Plan

Recipe cards can be added to the shopping list or meal plan. The app stores recipe IDs, so changing the language, guest count, or menu mode does not discard selections. Shopping-list quantities use the current guest count and are grouped by recipe. Meal-plan selections and completed cooking steps persist in `localStorage`.

The search, empty-results state, filters, meal-plan persistence, removing a planned recipe, cooking-step completion, timer controls, and language switching are useful E2E practice scenarios. Interactive controls use stable `data-testid` attributes.

## E2E Automation: pytest + Playwright

Dependencies are listed in `requirements.txt`. The tests use pytest-playwright and the synchronous Playwright API. `tests/conftest.py` starts Python's built-in HTTP server on an available local port, waits for `/index.html`, and shuts the server down after the test run. The `holiday_page` fixture creates a separate browser context for each test so `localStorage` and other state do not leak between scenarios.

### Page Object Model (POM)

- `pages/base_page.py` contains shared actions such as opening the page, locating elements by test ID, and waiting for visibility.
- `pages/holiday_feast_page.py` models app actions such as selecting a holiday or category, changing the guest count, adding a recipe, and opening the shopping list.
- Files in `tests/test_*.py` focus on scenarios and assertions rather than CSS implementation details.

Tests locate interactive elements by `data-testid`, for example `holiday-tab-tu-bav` and `guest-counter-input`. These selectors are independent of decorative CSS classes and translated text, making tests less fragile during localization and redesign. Playwright `expect` assertions automatically wait for visibility, state, and text conditions until the configured timeout.

### Existing Test Coverage

- `test_i18n.py`: English by default, switching to Hebrew, RTL direction, translated headings, switching back, and persistence after reload.
- `test_mode_switch.py`: the initial menu and Full Feast mode.
- `test_portion_calculator.py`: quantities for ten guests, nutrition totals, guest-count boundaries, and counter limits.
- `test_shopping_list.py`: multiple recipes, ingredient quantities in the drawer, and checking off purchased products.
- `test_holiday_navigation.py`: parameterized navigation across all nine holidays and their categories.

### What Happens During a pytest Run

1. Pytest discovers scenarios in `tests/` and creates the `app_url` fixture once per session.
2. The fixture starts a local server, and pytest-playwright launches a browser.
3. `holiday_page` creates an isolated browser context and opens the app through a Page Object.
4. A test calls readable POM actions such as `select_holiday("tu-bav")`.
5. `data-testid` locators interact with real elements; `expect` waits for the expected state and reports mismatches.
6. The browser context closes after each test, and the HTTP server shuts down after the session.

Boundary checks help catch minimum and maximum errors that ordinary values can miss. Toggling the language and reloading checks persistence. Changing the guest count while the shopping list is open checks that the drawer does not show stale quantities.

## Setup and Run

Python 3.10 or newer is required. From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest
```

To run a single test module:

```bash
python -m pytest tests/test_shopping_list.py -v
```

Open `index.html` directly in a browser to use the app. For E2E tests, do not start a server manually; the fixture starts and stops it.

## Interview Notes

**Short project overview:**

> I built an interactive guide to Israeli holidays alongside an E2E suite using Python and Playwright. The app supports English and Hebrew with RTL layout, nine holidays and recipe filters, two menu modes, serving calculations, and a shopping list. The tests use the Page Object Model: shared actions are separate from scenarios, locators use `data-testid`, and fixtures provide an isolated browser context and temporary local server. The suite covers more than happy paths, including counter boundaries, language persistence, nutrition calculations, and shopping-list updates. This demonstrates how to turn user requirements into repeatable browser checks.

**Testing concepts demonstrated:**

- Functional testing: filters, menu modes, language switching, and the shopping list.
- i18n/L10n: translations, HTML `lang`, RTL/LTR, and layout direction.
- UI behavior: key controls, selected states, drawer visibility, and recipe cards.
- Boundary testing: guest-count limits and counter constraints.
- E2E automation: a complete browser flow from the local HTTP server to assertions.
- Parameterized testing: consistent checks across holidays and categories.
- Cross-browser potential: the suite can be configured to run with Chromium, Firefox, and WebKit.

**Why use `data-testid` when CSS selectors are available?**

Test IDs provide a stable automation contract independent of visual structure and localized text. CSS selectors are still useful for visual checks, but test IDs are usually more robust for user workflows.

**How can RTL be checked in Playwright?**

Check `html[dir="rtl"]` and the document language, then inspect the computed direction of an important container with `getComputedStyle`. This catches cases where the attribute changes but the layout does not inherit the direction.

**How are serving quantities calculated?**

Each ingredient has a base quantity for two guests. The app multiplies it by `guests / 2`; Full Feast adds recipes without changing quantities for existing recipes. Tests can compare expected amounts and check the limits of 1 and 20 guests.

**What would you add before production?**

Verified recipe and nutrition data, aggregation of duplicate ingredients with unit normalization, accessibility tests, multi-browser CI, and visual checks across responsive layouts. Nutrition values are currently illustrative.
