@pytest.mark.sanity
def test_login(login: Page) -> None:
    expect(page.locator('[class="header-nav"]')).to_be_visible(timeout=15000)
    print("User logged in successfully.")