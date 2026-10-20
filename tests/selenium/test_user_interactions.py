from selenium.webdriver.common.by import By


def test_login_form_accepts_input(driver, base_url):
    driver.get(base_url + "/")
    driver.execute_script("window.localStorage.removeItem('token');")
    driver.get(base_url + "/login")
    email = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    captcha_input = driver.find_element(By.ID, "captcha-input")

    email.send_keys("demo@stockamock.test")
    password.send_keys("DemoPass1!")
    captcha_input.send_keys("ABC123")

    assert email.get_attribute("value") == "demo@stockamock.test"
    assert password.get_attribute("value") == "DemoPass1!"
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']")


def test_signup_form_shows_password_rules(driver, base_url):
    driver.get(base_url + "/signup")
    driver.find_element(By.ID, "name").send_keys("Demo User")
    driver.find_element(By.ID, "email").send_keys("demo@stockamock.test")
    driver.find_element(By.ID, "password").send_keys("DemoPass1!")

    checklist = driver.find_element(By.CSS_SELECTOR, "ul.checklist")
    assert "At least 8 characters" in checklist.text
    assert driver.find_element(By.ID, "name").get_attribute("value") == "Demo User"
