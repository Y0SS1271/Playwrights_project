import pytest
import time
from playwright.sync_api import Page, expect


ADMIN_URL = "https://sv-students-recommend.onrender.com/pages/admin.html"
RECOMMENDATION_DETAIL_URL = "https://sv-students-recommend.onrender.com/pages/recommendation-detail.html"
BASE_URL = "https://sv-students-recommend.onrender.com/pages/home.html"
DETAIL_URL = f"{BASE_URL}/pages/recommendation-detail.html"

# Selectors based on SRS Admin Management section (4.9, 4.10)
USER_MANAGEMENT_TABLE = '[data-test="admin-user-table"]'
BLACKLIST_INPUT = '[data-test="input-blacklist-email"], #blacklist-email'
BLACKLIST_SUBMIT_BTN = '[data-test="btn-add-blacklist"], #btn-blacklist'
DELETE_BY_ID_INPUT = '[data-test="input-rec-id"], #delete-rec-id'
DELETE_BY_ID_BTN = '[data-test="btn-delete-rec-by-id"]'
CONFIRM_DELETE_BTN = '[data-test="btn-confirm-ban"]'
SYSTEM_NAV_LINK = '[data-test="nav-system"]'


@pytest.mark.ui
@pytest.mark.sanity
@pytest.mark.smoke
def test_admin_page_access_granted_for_admin(admin_logged_in_page: Page) -> None:
    """
    Test Case 13: Verify Admin user can access System Management page.
    
    SRS Requirement: 2.2 / 3.4.2 / 4.9 - Admin has full access to system management.
    
    Steps:
    1. Authenticate as Admin via admin_logged_in_page fixture.
    2. Click on 'System' in the navigation bar or navigate to admin URL.
    3. Verify User Management and Blacklist sections are displayed.
    """
    page = admin_logged_in_page
    page.goto(ADMIN_URL)
    page.wait_for_load_state("networkidle")

    expect(page.locator("body")).to_contain_text("System Management", timeout=10000)
    expect(page.locator(USER_MANAGEMENT_TABLE)).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.security
def test_admin_page_access_denied_for_regular_user(logged_in_page: Page) -> None:
    """
    Test Case 14: Verify regular user is restricted from accessing the Admin page (RBAC).
    
    SRS Requirement: 2.1 / 2.2 / 3.2.1 - System link/page blocked/hidden for regular users.
    
    Steps:
    1. Authenticate as standard user via logged_in_page fixture.
    2. Ensure 'System' nav link is not visible or accessing admin URL redirects/shows 403 error.
    """
    page = logged_in_page
    
    # Verify 'System' option is hidden in header nav for standard user
    system_link = page.locator(SYSTEM_NAV_LINK)
    expect(system_link).not_to_be_visible()

    # Attempt direct navigation to admin page
    page.goto(ADMIN_URL)
    
    # Verify user is redirected away or shown access denied
    expect(page).not_to_have_url(ADMIN_URL)


@pytest.mark.ui
@pytest.mark.functional
def test_admin_delete_recommendation_by_uuid(admin_logged_in_page: Page) -> None:
    """
    Test Case 15: Verify Admin can delete any recommendation using UUID.
    
    SRS Requirement: 3.4.2 / 4.10 - Delete recommendation by ID.
    
    Steps:
    1. Navigate to Admin page.
    2. Enter a target recommendation UUID into the ID delete field.
    3. Click Delete button.
    4. Verify success response or notification.
    """
    page = admin_logged_in_page

    # Create a recommendation to ensure a valid UUID exists for deletion
    if not page.locator('[data-test="card-recommendation"]').first.is_visible():
        page.goto(RECOMMENDATION_DETAIL_URL)
        page.locator('[data-test="nav-signup-recommendations"]').click()
        page.locator('[data-test="input-recommendation-name"]').fill("John wick")
        page.locator('[data-test="input-recommender-name"]').click()
        page.locator('[data-test="input-recommender-name"]').fill("Yossi Ben Ezra")
        page.locator('[data-test="btn-submit-recommendation"]').click()
        card_body = page.locator('[class="card-body"]').first
        expect(card_body).to_contain_text("John wick by Yossi Ben Ezra", timeout=15000)

    rec_uuid = page.locator('[data-test="card-recommendation"]').first.get_attribute("data-id")

    page.goto(ADMIN_URL)
    page.wait_for_load_state("networkidle")

    delete_input = page.locator(DELETE_BY_ID_INPUT)
    delete_btn = page.locator(DELETE_BY_ID_BTN)
    conf_delete = page.locator(CONFIRM_DELETE_BTN)

    if delete_input.is_visible() and delete_btn.is_visible():
        delete_input.fill(rec_uuid)
        delete_btn.click()
        conf_delete.click()
        page.wait_for_timeout(1000)
        expect(page.locator("body")).to_be_visible()

    # Verfiy if the recommendation is deleted.
    page.goto(f"{RECOMMENDATION_DETAIL_URL}?id={rec_uuid}")
    page.wait_for_load_state("networkidle")
    expect(page.locator('[data-test="card-recommendation"]')).not_to_be_visible()


