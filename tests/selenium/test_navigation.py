from selenium.webdriver.common.by import By


def test_navigate_home_to_login(driver, base_url):
    driver.get(base_url + "/")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='home-login']").click()
    heading = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-heading']")
    assert heading.text == "Log In"
    assert "/login" in driver.current_url


def test_navigate_home_to_signup(driver, base_url):
    driver.get(base_url + "/")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='home-signup']").click()
    heading = driver.find_element(By.CSS_SELECTOR, "[data-testid='signup-heading']")
    assert heading.text == "Create New Account"
    assert "/signup" in driver.current_url


def test_login_to_signup_link(driver, base_url):
    driver.get(base_url + "/login")
    driver.find_element(By.CSS_SELECTOR, "span.signup a").click()
    heading = driver.find_element(By.CSS_SELECTOR, "[data-testid='signup-heading']")
    assert heading.is_displayed()
