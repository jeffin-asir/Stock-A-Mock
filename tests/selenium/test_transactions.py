from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_transaction_page(driver, base_url, path):
    # Seed a token on the frontend origin before opening the protected page.
    driver.get(base_url + "/")
    driver.execute_script("window.localStorage.setItem('token', 'selenium-test-token');")
    driver.get(base_url + path)

    return WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".stock-card"))
    )


def submit_transaction(driver, card, quantity, button_label, expected_message):
    card.find_element(By.CSS_SELECTOR, "input[type='number']").send_keys(str(quantity))
    card.find_element(By.XPATH, f".//button[normalize-space()='{button_label}']").click()

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    message = WebDriverWait(driver, 12).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".message"))
    )
    assert message.text == expected_message


def test_buy_stock(driver, base_url):
    card = open_transaction_page(driver, base_url, "/buy")
    assert card.find_element(By.TAG_NAME, "h3").text == "AAPL"

    submit_transaction(driver, card, 2, "Buy More", "Bought 2 of AAPL")


def test_sell_stock(driver, base_url):
    card = open_transaction_page(driver, base_url, "/sell")
    assert card.find_element(By.TAG_NAME, "h3").text == "AAPL"

    submit_transaction(driver, card, 2, "Sell", "Sold 2 of AAPL")
