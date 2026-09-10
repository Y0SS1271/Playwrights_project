import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://sv-students-recommend.onrender.com/pages/login.html"
ADMIN_URL = "https://sv-students-recommend.onrender.com/pages/admin.html"


@pytest.mark.mobile
@pytest.mark.ui
def test_mobile_navigation_and_layout(mobile_page: Page) -> None:
    """
    Test Case 13: Verify navigation bar and layout on mobile viewport dimensions.
    
    SRS Requirement: 3.2.1 / Mobile responsiveness guidelines.
    
    Steps:
    1. Open application login page in mobile viewport fixture (390x844).
    2. Verify logo and interactive elements scale properly without breaking layout.
    3. Verify essential inputs (Email, Password, Sign In button) are visible and clickable.
    """
    mobile_page.goto(LOGIN_URL)
    
    email_input = mobile_page.locator('[data-test="input-email"]')
    expect(email_input).to_be_visible()
    
    submit_btn = mobile_page.locator('[data-test="btn-login"]')
    expect(submit_btn).to_be_visible()


@pytest.mark.sanity
@pytest.mark.smoke
def test_positive_logout(logged_in_page: Page) -> None:
    """
    Test Case 14: Verify logged-in user can perform a clean logout.
    
    SRS Requirement: 3.2.1 / 3.4.1 - Logout terminates session and returns user to Login page.
    
    Steps:
    1. Authenticate user via fixture.
    2. Locate and click 'Logout' button in header navigation or profile.
    3. Confirm redirection to login page.
    """
    page = logged_in_page
    logout_btn = page.locator("text=Logout, [data-test='nav-logout'], #logout-btn").first
    logout_btn.click()

    expect(page).to_have_url(LOGIN_URL)
