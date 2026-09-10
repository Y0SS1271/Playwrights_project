import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page, Playwright

#from Tests.test_registration import REGISTER_URL
load_dotenv()

BASE_URL = "https://sv-students-recommend.onrender.com"
REGISTER_URL = f"{BASE_URL}/pages/register.html"


@pytest.fixture
def user_credentials() -> dict:
    """Returns the credentials for a regular user, loaded from environment variables."""
    return {
        "email": os.getenv("TEST_USER_EMAIL"),
        "password": os.getenv("TEST_USER_PASSWORD")
    }

@pytest.fixture
def admin_credentials() -> dict:
    """Returns the credentials for an administrator user, loaded from environment variables."""
    return {
        "email": os.getenv("TEST_ADMIN_EMAIL"),
        "password": os.getenv("TEST_ADMIN_PASSWORD")
    }

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

    yield page  # Hand over control to the test function
    page.close


@pytest.fixture
def logged_in_page(page: Page, user_credentials: dict) -> Page:
    """
    Fixture that performs login as a regular user and returns the logged-in page.
    """
    page.goto(f"{BASE_URL}/pages/login.html")
    page.locator('[data-test="input-email"]').fill(user_credentials["email"])
    page.locator('[data-test="input-password"]').fill(user_credentials["password"])
    page.locator('[data-test="btn-login"]').click()
    page.wait_for_selector('[class="header-nav"], .nav-container, body', state="visible")

    # Hand over control to the test function
    yield page
    
    # Teardown Phase: Logout execution after test finishes
    try:
        logout_btn = page.locator("text=Logout, [data-test='nav-logout'], #logout-btn").first
        if logout_btn.is_visible():
            logout_btn.click()
            page.wait_for_url(f"{BASE_URL}/pages/login.html", timeout=5000)
    except Exception:
        # Prevent fixture teardown failure if test already logged out or changed state
        pass
    finally:
        page.close()

@pytest.fixture
def admin_logged_in_page(page: Page, admin_credentials: dict) -> Page:
    """
    Fixture that performs login as an administrator user and returns the logged-in page.
    """
    page.goto(f"{BASE_URL}/pages/login.html")
    page.locator('[data-test="input-email"]').fill(admin_credentials["email"])
    page.locator('[data-test="input-password"]').fill(admin_credentials["password"])
    page.locator('[data-test="btn-login"]').click()
    page.wait_for_selector('[class="header-nav"], .nav-container, body', state="visible")

    # Hand over control to the test function
    yield page

    # Teardown Phase: Logout execution after test finishes
    try:
        logout_btn = page.locator("text=Logout, [data-test='nav-logout'], #logout-btn").first
        if logout_btn.is_visible():
            logout_btn.click()
            page.wait_for_url(f"{BASE_URL}/pages/login.html", timeout=5000)
    except Exception:
        # Prevent fixture teardown failure if test already logged out or changed state
        pass
    finally:
        page.close()