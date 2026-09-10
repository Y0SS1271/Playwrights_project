import pytest
from playwright.sync_api import Page, Playwright, expect


@pytest.mark.sanity
def test_add_recommendation(login: Page) -> None:
    """Verify that a logged-in user can add a recommendation. (SRS 3.3.3)
    
    Args:
        login (Page): The logged-in Playwright page object.
    """
    page = login


    page.locator('[data-test="nav-signup-recommendations"]').click()
    page.locator('[data-test="input-recommendation-name"]').fill("John wick")
    page.locator("[data-test=\"input-recommender-name\"]").click()
    page.locator("[data-test=\"input-recommender-name\"]").fill("Yossi Ben Ezra")
    page.locator('[data-test="btn-submit-recommendation"]').click()

    '''
    Verify that the recommendation was added successfully by checking if
    the recommendation name appears in the list of recommendations.
    '''

    recommendation_name = page.locator('[class="card-body"]').first
    expect(recommendation_name).to_contain_text("John wick by Yossi Ben Ezra", timeout=15000)

@pytest.mark.sanity
def test_delete_recommendation(login: Page) -> None:
    """Verify that a logged-in user can delete a recommendation. (Not mentioned in SRS, but a good test to have)
    Args:
        login (Page): The logged-in Playwright page object.
    """
    page = login
    # Click on the first recommendation in the list (which is the one that created here) to view its details
    page.locator('[class="card-body"]').first.click()

    # Click on the delete button for the first recommendation in the list
    page.locator('[data-test="btn-delete-recommendation"]').click()
    page.locator('[data-test="btn-confirm-delete"]').click()

        # Verify that the recommendation was deleted successfully by checking if
        # the recommendation name no longer appears in the list of recommendations.
    recommendation_name = page.locator('[class="card-body"]').first
    expect(recommendation_name).not_to_contain_text("John wick by Yossi Ben Ezra", timeout=15000)
   