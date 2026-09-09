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


def get_login_token(playwright: Playwright) -> str:
    """Verify that the login API returns a valid auth token.

    Steps:
    - Send a POST request to /auth/login with valid credentials
    - Confirm the response status is successful
    - Extract the auth token from the response body and store it globally
    """
    global token

    request_context = playwright.request.new_context(base_url=BASE_URL)
    response = request_context.post(
        "/auth/login",
        data={
            "email": "hagai.tregerman@gmail.com",
            "password": "test1234",
        },
    )

    assert response.ok, f"Login request failed: {response.status} {response.text()}"

    body = response.json()
    token = body.get("token") or body.get("accessToken") or body.get("access_token")
    
    request_context.dispose()
    return token


def login(page: Page) -> Page:
    """Fixture to log in a user before running the test.
    
    Args:
        page (Page): The Playwright page object.
        
    Returns:
        Page: The logged-in Playwright page object.
    """
    page.goto("https://sv-students-recommend.onrender.com/pages/login.html")
    page.locator('[data-test="input-email"]').fill("yossibenezra20@gmail.com")
    page.locator('[data-test="input-password"]').fill("test13")
    page.locator('[data-test="btn-login"]').click()

    return page