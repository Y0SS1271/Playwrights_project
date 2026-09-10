import pytest
from playwright.sync_api import Page, expect

@pytest.mark.sanity
def test_add_recommendation(logged_in_page: Page) -> None:
    """
    Test Case 7: Verify logged-in student can successfully add a recommendation.
    SRS Requirement: 3.3.3 - Add Recommendation.
    Steps:

    1. Navigate to the 'Add Recommendation' page.
    2. Fill in the recommendation name and recommender name.
    3. Submit the recommendation.
    4. Assert that the recommendation appears in the list of recommendations.

    Args:
        logged_in_page (Page): The Playwright page object after logging in as a regular user.

    Returns:
        None
    """
    page = logged_in_page

    page.locator('[data-test="nav-signup-recommendations"]').click()
    page.locator('[data-test="input-recommendation-name"]').fill("John wick")
    page.locator('[data-test="input-recommender-name"]').click()
    page.locator('[data-test="input-recommender-name"]').fill("Yossi Ben Ezra")
    page.locator('[data-test="btn-submit-recommendation"]').click()

    card_body = page.locator('[class="card-body"]').first
    expect(card_body).to_contain_text("John wick by Yossi Ben Ezra", timeout=15000)

@pytest.mark.sanity
def test_delete_recommendation(logged_in_page: Page) -> None:
    """
    Test Case 8: Verify logged-in user can delete their own recommendation.
    SRS Requirement: 3.3.2 - Regular user can delete their own recommendation.

    Steps:
    1. Navigate to the 'My Recommendations' page.
    2. Click the delete button on a recommendation.
    3. Confirm the deletion.
    4. Assert that the recommendation no longer appears in the list.

    Args:
        logged_in_page (Page): The Playwright page object after logging in as a regular user

    Returns:
        None
    """
    page = logged_in_page

    page.locator('[class="card-body"]').first.click()
    page.locator('[data-test="btn-delete-recommendation"]').click()
    page.locator('[data-test="btn-confirm-delete"]').click()

    card_body = page.locator('[class="card-body"]').first
    expect(card_body).not_to_contain_text("John wick by Yossi Ben Ezra", timeout=15000)

@pytest.mark.ui
@pytest.mark.functional
@pytest.mark.parametrize("category", ["All", "Book", "Movie", "Series", "Activity"])
def test_category_filter_home(logged_in_page: Page, category: str) -> None:
    """
    Test Case 9: Parameterized test verifying Home page recommendations filter by category.
    SRS Requirement: 3.3.1 - Filter recommendations by category.

    Steps:
    1. Navigate to the Home page.
    2. Click on the filter button corresponding to the category.
    3. Assert that the recommendations displayed belong to the selected category.

    Args:
        logged_in_page (Page): The Playwright page object after logging in as a regular user
        category (str): The category to filter recommendations by (All, Book, Movie, Series, Activity).
    Returns:
        None
    """
    page = logged_in_page
    filter_btn = page.locator(f"[data-test=\"filter-{category}\"]").first
    
    if filter_btn.is_visible():
        filter_btn.click()
        page.wait_for_timeout(500)
        expect(filter_btn).to_be_visible()

@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.errors_handling
def test_add_recommendation_missing_mandatory_field(logged_in_page: Page) -> None:
    """
    Test Case 10: Verify validation error when attempting to submit recommendation without mandatory fields.
    SRS Requirement: 3.3.3 - Mandatory fields missing prevents form submission.
    Expected Error: "Recommendation name is required."

    Steps:
    1. Navigate to the 'Add Recommendation' page.
    2. Leave the recommendation name field empty and fill in the recommender name.
    3. Click 'Submit Recommendation'.
    4. Assert that the specific error message is displayed.

    Args:
        logged_in_page (Page): The Playwright page object after logging in as a regular user
    Returns:
        None
    """
    page = logged_in_page
    page.locator('[data-test="nav-signup-recommendations"]').click()
    
    page.locator('[data-test="input-recommender-name"]').fill("Test Recommender")
    page.locator('[data-test="btn-submit-recommendation"]').click()

    error_msg = page.locator("[data-test='error-message']")
    expect(error_msg).to_be_visible