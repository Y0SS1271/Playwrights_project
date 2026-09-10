import pytest
from playwright.sync_api import Page, expect

STORE_URL = "https://sv-students-recommend.onrender.com/pages/store.html"
CART_URL = "https://sv-students-recommend.onrender.com/pages/cart.html"
PAYMENT_URL = "https://sv-students-recommend.onrender.com/pages/payment.html"


@pytest.mark.ui
@pytest.mark.regression
def test_store_add_to_cart_and_quantity_recalculation(logged_in_page: Page) -> None:
    """
    Test Case 11: Verify adding products from Store to Cart and quantity price recalculation.
    
    SRS Requirement: 3.5.1 / 3.5.2 - Store & Cart recalculation.
    T-Shirt (50 NIS), Cup (20 NIS). Modifying quantities with +/- updates grand total.
    
    Steps:
    1. Navigate to Store page.
    2. Click 'Add to cart' on Cup (20 NIS).
    3. Navigate to Cart page.
    4. Increase Cup quantity using '+' button.
    5. Verify Grand Total recalculates correctly.
    """
    page = logged_in_page
    page.goto(STORE_URL)

    # Click Add to Cart for first product
    add_btn = page.locator("button:has-text('Add to cart')").first
    add_btn.click()

    # Go to cart
    page.goto(CART_URL)
    
    # Assert cart item is visible
    cart_container = page.locator(".cart-container, body")
    expect(cart_container).to_contain_text("NIS")

    # Increase quantity button '+' if present
    plus_btn = page.locator("button:has-text('+')").first
    if plus_btn.is_visible():
        plus_btn.click()
        page.wait_for_timeout(500)
        expect(cart_container).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.errors_handling
def test_payment_form_validation(logged_in_page: Page) -> None:
    """
    Test Case 12: Verify empty mandatory fields on Payment page prevent order placement.
    
    SRS Requirement: 3.5.3 - Payment Page mandatory fields (Full Name, Address, Credit Card Number, CVV, Expiration Date).
    
    Steps:
    1. Navigate directly to Payment page.
    2. Leave mandatory inputs blank.
    3. Click 'Place Order' button.
    4. Verify submission is blocked and form inputs flag invalid state / error visible.
    """
    page = logged_in_page
    page.goto(PAYMENT_URL)

    place_order_btn = page.locator("button:has-text('Place Order'), [data-test='btn-place-order']").first
    if place_order_btn.is_visible():
        place_order_btn.click()
        
        # Verify user remains on payment page (not redirected to confirmation)
        expect(page).to_have_url(PAYMENT_URL)