import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
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


@pytest.mark.sanity
def test_add_recommendation(login: Page) -> None:
    """Verify that a logged-in user can add a recommendation. (SRS 3.3.3)
    
    Args:
        login (Page): The logged-in Playwright page object.
    """
    page = login


    page.locator('[data-test="nav-signup-recommendations"]').click()
    page.locator('[data-test="input-recommendation-name"]').fill("John wick")
    page.locator('[data-test="btn-submit-recommendation"]').click()

    '''
    Verify that the recommendation was added successfully by checking if
    the recommendation name appears in the list of recommendations.
    '''

    recommendation_name = page.locator('[data-test="card-title"]').first
    expect(recommendation_name).to_have_text("John wick", timeout=15000)
