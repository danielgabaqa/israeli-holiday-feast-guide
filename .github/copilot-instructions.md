# Workspace Setup

- [x] Verify that this instruction file exists in `.github/`.
- [x] Clarify project requirements: standalone HTML app with Python 3.10+ pytest-playwright E2E tests.
- [x] Scaffold the project: app, POM pages, fixtures, scenario tests, dependencies, and guide created.
- [x] Customize the project: bilingual holiday app, responsive controls, portion calculations, macro summary, and shopping list implemented.
- [x] Install required extensions: none specified for this static HTML and Python test project.
- [x] Compile and validate: embedded JavaScript parsed; 15 Playwright E2E tests passed using Chromium.
- [x] Create and run a task: not needed; the app is a standalone HTML file and the test command is documented.
- [x] Launch the project: no persistent server started; tests start and stop their own local server.
- [x] Ensure documentation is complete: `README.md` contains architecture, run instructions, test coverage, and interview guide.

## Project Notes

- The application entry point is `index.html`.
- Install Python dependencies with `python -m pip install -r requirements.txt`.
- Install a browser with `python -m playwright install chromium`.
- Run the E2E suite with `python -m pytest`.
- Recipe calorie and macro values are illustrative sample data, not dietary advice.
