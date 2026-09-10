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
    email = "hagai.tregerman@gmail.com"
    password = "test1234"

    if not email or not password:
        pytest.fail(
            "User credentials are missing."
        )

    return {
        "email": email,
        "password": password,
    }



@pytest.fixture
def admin_credentials() -> dict:
    """Returns the credentials for an administrator user, loaded from environment variables."""
    return {
        "email": os.getenv("TEST_ADMIN_EMAIL"),
        "password": os.getenv("TEST_ADMIN_PASSWORD")
    }
import pytest
from playwright.sync_api import Page, Playwright


BASE_URL = "https://sv-students-recommend.onrender.com"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def logged_in_page(
    page: Page,
    user_credentials: dict,
    base_url: str,
) -> Page:

    page.goto(f"{base_url}/pages/login.html")

    page.locator('[data-test="input-email"]').fill(
        user_credentials["email"]
    )

    page.locator('[data-test="input-password"]').fill(
        user_credentials["password"]
    )

    page.locator('[data-test="btn-login"]').click()

    yield page  # Hand over control to the test function
    page.close


@pytest.fixture
def logged_in_page(page: Page, user_credentials: dict) -> Page:
    page.goto(f"{BASE_URL}/pages/login.html")

    page.locator('[data-test="input-email"]').fill(
        user_credentials["email"]
    )
    page.locator('[data-test="input-password"]').fill(
        user_credentials["password"]
    )

    page.locator('[data-test="btn-login"]').click()

    # IMPORTANT: verify authentication actually succeeded
    page.wait_for_load_state("networkidle")

    error_message = page.get_by_text(
        "Incorrect email or password",
        exact=False
    )

    if error_message.is_visible():
        pytest.fail(
            "User login failed: invalid user credentials."
        )

    return page


@pytest.fixture
def admin_logged_in_page(page: Page, admin_credentials: dict) -> Page:
    """Log in as an administrator and return the authenticated page."""

    page.goto(f"{BASE_URL}/pages/login.html")

    page.locator('[data-test="input-email"]').fill(
        admin_credentials["email"]
    )
    page.locator('[data-test="input-password"]').fill(
        admin_credentials["password"]
    )

    page.locator('[data-test="btn-login"]').click()

    # Wait for either successful navigation or the login error.
    page.wait_for_load_state("networkidle")

    error_message = page.get_by_text(
        "Incorrect email or password",
        exact=False
    )

    if error_message.is_visible():
        pytest.fail(
            "Admin login failed: the application rejected the supplied "
            "admin email/password."
        )

    yield page

    # Teardown
    try:
        logout_btn = page.locator(
            "text=Logout, [data-test='nav-logout'], #logout-btn"
        ).first

        if logout_btn.is_visible():
            logout_btn.click()
            page.wait_for_url(
                f"{BASE_URL}/pages/login.html",
                timeout=5000
            )
    except Exception:
        pass


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
    return page


@pytest.fixture
def mobile_page(playwright: Playwright) -> Page:

    browser = playwright.chromium.launch()

    context = browser.new_context(
        viewport={
            "width": 390,
            "height": 844,
        },
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/14.0.3 Mobile/15E148 Safari/604.1"
        ),
    )

    page = context.new_page()

    yield page

    context.close()
    browser.close()


@pytest.fixture
def register_page(page: Page, base_url: str) -> Page:
    page.goto(f"{base_url}/pages/register.html")
    page.wait_for_load_state("domcontentloaded")
    return page
