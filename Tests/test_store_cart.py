import pytest
from playwright.sync_api import Page, expect

STORE_URL = "https://sv-students-recommend.onrender.com/pages/store.html"
CART_URL = "https://sv-students-recommend.onrender.com/pages/cart.html"
PAYMENT_URL = "https://sv-students-recommend.onrender.com/pages/payment.html"


@pytest.mark.ui
@pytest.mark.functional
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

    # Clean up: Ensure Cart is empty before test
    page.locator('[data-test="nav-cart"]').click()
    page.wait_for_load_state("networkidle")
    if page.locator('[data-test="btn-remove-cup"]').is_visible():
        page.locator('[data-test="btn-remove-cup"]').click()
        page.wait_for_timeout(2000)  # Wait for cart update

    # 1. Navigate to Store page
    page.goto(STORE_URL)
    page.wait_for_load_state("networkidle")

    
    # 2. Click 'Add to cart' on Cup (20 NIS)
    page.locator('[data-test="btn-add-cup"]').click()
    page.locator('[data-test="cart-badge"]').wait_for(state="visible")  # Wait for cart badge to update  

    # 3. Navigate to Cart page
    page.locator('[data-test="nav-cart"]').click()
    page.wait_for_load_state("networkidle")
    
    # 4. Increase Cup quantity using '+' button
    page.locator('[data-test="btn-qty-plus-cup"]').click()
    
    # 5. Verify Grand Total recalculates correctly (20 NIS * 2 = 40 NIS)
    expect(page.locator('[data-test="cart-subtotal-cup"]')).to_contain_text("40")


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
    page.wait_for_load_state("networkidle")

    place_order_btn = page.locator("[data-test='btn-place-order']")
    if place_order_btn.is_visible():
        place_order_btn.click()
        
        # Verify that the payment error message is visible
        expect(page.locator("#paymentError")).to_be_visible()