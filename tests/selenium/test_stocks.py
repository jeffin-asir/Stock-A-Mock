from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_stock_data_is_retrieved_and_searchable(driver, base_url):
    driver.get(base_url + "/search")
    wait = WebDriverWait(driver, 12)

    aapl = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stock-card-AAPL']"))
    )
    assert "AAPL" in aapl.text
    assert "Current Price" in aapl.text

    search = driver.find_element(By.CSS_SELECTOR, "[data-testid='stock-search']")
    search.clear()
    search.send_keys("TSLA")

    tsla = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stock-card-TSLA']"))
    )
    assert tsla.is_displayed()
    assert len(driver.find_elements(By.CSS_SELECTOR, ".stock-card")) == 1
