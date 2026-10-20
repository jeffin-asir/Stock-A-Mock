from selenium.webdriver.common.by import By


def test_home_page_loads(driver, base_url):
    driver.get(base_url + "/")
    title = driver.find_element(By.CSS_SELECTOR, "[data-testid='app-title']")
    assert title.text == "Stock-A-Mock"
    assert "Login" in driver.page_source
    assert "Sign up" in driver.page_source
