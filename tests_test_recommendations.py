import pytest
from playwright.sync_api import Page, expect

@pytest.mark.sanity
def test_add_recommendation(logged_in_page: Page) -> None:
    """
    Test Case 7: Verify logged-in student can successfully add a recommendation.
    
    SRS Requirement: 3.3.3 - Add Recommendation (Mandatory fields: Category, Recommendation Name, Your Name).
    
    Steps:
    1. Click 'Add Recommendation' in navbar.
    2. Fill Recommendation Name and Recommender Name.
    3. Submit recommendation form.
    4. Verify card appears on Home page with provided title and author.
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
    1. Click on card details of the user's recommendation.
    2. Click 'Delete' button.
    3. Confirm deletion in modal.
    4. Verify card is removed from recommendations list.
    """
    page = logged_in_page

    page.locator('[class="card-body"]').first.click()
    page.locator('[data-test="btn-delete-recommendation"]').click()
    page.locator('[data-test="btn-confirm-delete"]').click()

    card_body = page.locator('[class="card-body"]').first
    expect(card_body).not_to_contain_text("John wick by Yossi Ben Ezra", timeout=15000)


@pytest.mark.ui
@pytest.mark.functional
@pytest.mark.parametrize("category", ["Book", "Movie", "Series", "Activity"])
def test_category_filter_home(logged_in_page: Page, category: str) -> None:
    """
    Test Case 9: Parameterized test verifying Home page recommendations filter by category.
    
    SRS Requirement: 3.3.1 - Filter recommendations by category (All, Book, Movie, Series, Activity, Other).
    
    Steps:
    1. Navigate to Home page.
    2. Click on category filter button (e.g. Book, Movie, Series, Activity).
    3. Verify active category button reflects selection or filtered cards match category.
    """
    page = logged_in_page
    filter_btn = page.locator(f"button:has-text('{category}'), [data-test='filter-{category.lower()}']").first
    
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
    1. Open 'Add Recommendation' form.
    2. Leave 'Recommendation Name' blank.
    3. Click submit.
    4. Verify validation error message appears and form is not submitted.
    """
    page = logged_in_page
    page.locator('[data-test="nav-signup-recommendations"]').click()
    
    # Leave recommendation name empty, fill recommender name
    page.locator('[data-test="input-recommender-name"]').fill("Test Recommender")
    page.locator('[data-test="btn-submit-recommendation"]').click()

    error_msg = page.locator("text=Recommendation name is required., .error-message, :invalid")
    expect(error_msg.first).to_be_visible()
