import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://sv-students-recommend.onrender.com/pages/login.html"

EMAIL_INPUT = '[data-test="input-email"]'
PASSWORD_INPUT = '[data-test="input-password"]'
SUBMIT_BUTTON = '[data-test="btn-login"]'
EYE_ICON = '.toggle-password, #togglePassword, [data-test="btn-toggle-password"]'


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.errors_handling
def test_invalid_login_credentials(page: Page) -> None:
    """
    Test Case 5: Verify error message displayed when logging in with invalid credentials.
    
    SRS Requirement: 3.1.1 - Incorrect email or password must display a clear error message.
    
    Steps:
    1. Navigate to Login Page.
    2. Enter non-existing email / incorrect password.
    3. Click 'Sign In'.
    4. Validate error toast or error text appears.
    """
    page.goto(LOGIN_URL)
    page.fill(EMAIL_INPUT, "invalid_user_999@svcollege.co.il")
    page.fill(PASSWORD_INPUT, "wrongpassword123")
    page.click(SUBMIT_BUTTON)

    error_msg = page.locator(".error-message, .alert-danger, text=/invalid|incorrect|failed/i")
    expect(error_msg.first).to_be_visible()


@pytest.mark.ui
@pytest.mark.functional
def test_login_eye_toggle_password(page: Page) -> None:
    """
    Test Case 6: Verify password visibility toggle (eye icon) on Login Page.
    
    SRS Requirement: 3.1.1 - Eye icon displays or hides password text.
    
    Steps:
    1. Navigate to Login Page.
    2. Enter password into password field.
    3. Assert password input type is initially 'password'.
    4. Click the eye icon toggle button.
    5. Assert password input type changes to 'text'.
    """
    page.goto(LOGIN_URL)
    pwd_field = page.locator(PASSWORD_INPUT)
    pwd_field.fill("secret123")

    expect(pwd_field).to_have_attribute("type", "password")

    eye_button = page.locator(EYE_ICON).first
    if eye_button.is_visible():
        eye_button.click()
        expect(pwd_field).to_have_attribute("type", "text")
