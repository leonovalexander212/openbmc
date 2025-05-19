import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

URL = "https://localhost:2443"
USERNAME = "root"
PASSWORD = "0penBmc"
BAD_PASSWORD = "wrongpass"
BAD_USERNAME = "wronguser"

USERNAME_FIELD = (By.ID, "username")
PASSWORD_FIELD = (By.ID, "password")
LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='login-button-submit']")
ERROR_MESSAGE = (By.CSS_SELECTOR, ".login-error")

@pytest.fixture()
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(URL)
    try:
        browser.find_element(By.ID, "details-button").click()
        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.ID, "proceed-link"))
        ).click()
    except:
        pass
    yield browser
    browser.quit()

def login(browser, username, password):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(USERNAME_FIELD)
    ).send_keys(username)
    browser.find_element(*PASSWORD_FIELD).send_keys(password)
    browser.find_element(*LOGIN_BUTTON).click()

def test_successful_login(driver):
    login(driver, USERNAME, PASSWORD)
    assert WebDriverWait(driver, 10).until(
        EC.url_changes(URL)
    ), "Не удалось войти с правильными данными"

def test_invalid_login(driver):
    login(driver, BAD_USERNAME, BAD_PASSWORD)
    assert WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(ERROR_MESSAGE)
    ), "Ошибка не отображается при вводе неверных данных"

def test_account_lockout(driver):
    for _ in range(5):
        login(driver, USERNAME, BAD_PASSWORD)
        sleep(1)
        driver.refresh()
    login(driver, USERNAME, PASSWORD)
    try:
        WebDriverWait(driver, 5).until(EC.url_changes(URL))
        assert False, "Вход разрешён, блокировка не предусмотрена"
    except TimeoutException:
        pass
