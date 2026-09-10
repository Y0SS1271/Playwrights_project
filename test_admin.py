import pytest
from playwright.sync_api import Page, expect


@pytest.mark.sanity
def test_admin_login(admin_logged_in_page: Page) -> None:
    """
    Verify that the admin can successfully log in.
    """
    page = admin_logged_in_page

    # Login must not leave us on the login page.
    expect(page).not_to_have_url(
        "https://sv-students-recommend.onrender.com/pages/login.html",
        timeout=15000,
    )

    print("Admin logged in successfully.")


@pytest.mark.sanity
def test_admin_dashboard(admin_logged_in_page: Page) -> None:
    """
    Verify that the admin dashboard is displayed
    after successful login.
    """
    page = admin_logged_in_page

    # Verify that we are no longer on the login page.
    expect(page).not_to_have_url(
        "https://sv-students-recommend.onrender.com/pages/login.html",
        timeout=15000,
    )

    # The page itself must be visible.
    expect(page.locator("body")).to_be_visible(timeout=15000)

    print("Admin dashboard is displayed successfully.")


@pytest.mark.sanity
def test_admin_can_access_recommendations(
    admin_logged_in_page: Page,
) -> None:
    """
    Verify that an authenticated admin can access
    the recommendations area.
    """
    page = admin_logged_in_page

    # Verify that the admin is actually logged in.
    expect(page).not_to_have_url(
        "https://sv-students-recommend.onrender.com/pages/login.html",
        timeout=15000,
    )

    # Look for a recommendations link/button.
    recommendation_link = page.get_by_text(
        "Recommendations",
        exact=True,
    )

    expect(recommendation_link).to_be_visible(timeout=15000)
    recommendation_link.click()

    expect(page.locator("body")).to_be_visible(timeout=15000)

    print("Admin can access recommendations successfully.")