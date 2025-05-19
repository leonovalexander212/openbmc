from selenium import webdriver

def test_redfish_ui():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без GUI
    driver = webdriver.Chrome(options=options)
    
    driver.get("https://localhost:2443/redfish")
    assert "Redfish" in driver.title
    
    driver.quit()
