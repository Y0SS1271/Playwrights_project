import pytest
import re
from playwright.sync_api import Page, expect

# ----------------------------------------------------------------------
# Constants & Selectors
# ----------------------------------------------------------------------
REGISTER_URL = "https://sv-students-recommend.onrender.com/pages/register.html"

# Selectors based on the UI layout (SRS Section 4.2)
NAME_INPUT = '[data-test="input-name"]'
EMAIL_INPUT = 'input[type="email"]'
PASSWORD_INPUT = 'input[type="password"]'
SUBMIT_BUTTON = 'button:has-text("Create Account")'
GOOGLE_BUTTON = 'button:has-text("Continue with Google")'


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def register_page(page: Page) -> Page:
    """
    Fixture to navigate to the registration page before each test execution.
    Provides a clean state for every test case.

    Args:
        page (Page): The Playwright page fixture for browser automation.

    Returns:
        Page: The Playwright page object navigated to the registration URL.
    """
    page.goto(REGISTER_URL)
    page.wait_for_load_state("networkidle")
    return page


# ----------------------------------------------------------------------
# Test Cases
# ----------------------------------------------------------------------

@pytest.mark.ui
@pytest.mark.smoke
def test_register_page_elements_visibility(register_page: Page) -> None:
    """
    Test Case: Verify UI elements visibility on Registration Page.
    
    SRS Requirement: 3.1.2 - Registration Page layout.
    
    Steps:
    1. Navigate to the registration page via fixture.
    2. Verify presence of Student Name, Email, Password inputs, submit button, and Google login option.

    Args:
        register_page (Page): Navigated Playwright page provided by the fixture.

    Returns:
        None
    """
    expect(register_page.locator(NAME_INPUT)).to_be_visible()
    expect(register_page.locator(EMAIL_INPUT)).to_be_visible()
    expect(register_page.locator(PASSWORD_INPUT)).to_be_visible()
    expect(register_page.locator(SUBMIT_BUTTON)).to_be_visible()
    expect(register_page.locator(GOOGLE_BUTTON)).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.boundary
def test_register_short_password_validation(register_page: Page) -> None:
    """
    Test Case: Verify error message when registering with a password under 6 characters.
    
    SRS Requirement: 3.1.2 - Password must be at least 6 characters.
    Expected Error: "Password should be at least 6 characters."
    
    Steps:
    1. Fill valid Student Name and Email.
    2. Fill a short password (less than 6 characters, e.g., "test1").
    3. Click 'Create Account'.
    4. Assert that the specific error message is displayed.

    Args:
        register_page (Page): Navigated Playwright page provided by the fixture.

    Returns:
        None
    """
    register_page.fill(NAME_INPUT, "Test Student")
    register_page.fill(EMAIL_INPUT, "valid.student@svcollege.co.il")
    register_page.fill(PASSWORD_INPUT, "test1")  # 5 characters (Invalid)
    
    register_page.click(SUBMIT_BUTTON)
    
    error_locator = register_page.locator("text=Password should be at least 6 characters.")
    expect(error_locator).to_be_visible()


@pytest.mark.sanity
def test_successful_registration(register_page: Page) -> None:
    """
    Test Case: Verify successful student registration with valid credentials.
    
    SRS Requirement: 3.1.2 - Valid registration flow.
    
    Steps:
    1. Fill valid Student Name, unique Email, and valid Password (6+ alphanumeric chars).
    2. Click 'Create Account'.
    3. Verify user is redirected to login page or home page.

    Args:
        register_page (Page): Navigated Playwright page provided by the fixture.

    Returns:
        None
    """
    import time
    unique_email = f"student.{int(time.time())}@svcollege.co.il"
    
    register_page.fill(NAME_INPUT, "Test Student")
    register_page.fill(EMAIL_INPUT, unique_email)
    register_page.fill(PASSWORD_INPUT, "test12")  # Valid password matching spec example
    
    register_page.click(SUBMIT_BUTTON)
    
    expect(register_page).to_have_url(re.compile(r".*(login|home)\.html"))


@pytest.mark.integration
@pytest.mark.functional
def test_continue_with_google_button(register_page: Page) -> None:
    """
    Test Case: Verify 'Continue with Google' button is interactive.
    
    SRS Requirement: 3.1.2 / 3.1.3 - OAuth via Google.
    
    Steps:
    1. Locate the 'Continue with Google' button.
    2. Ensure the button is enabled and clickable.

    Args:
        register_page (Page): Navigated Playwright page provided by the fixture.

    Returns:
        None
    """
    google_btn = register_page.locator(GOOGLE_BUTTON)
    expect(google_btn).to_be_enabled()