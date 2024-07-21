from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def open_firefox():
    options = Options()
    
    service = Service(executable_path="/snap/bin/geckodriver")
    profile = FirefoxProfile()

  #  profile.set_preference("javascript.enabled", False)

    options.profile = profile
    
    driver = webdriver.Firefox(options=options, service=service)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.get("https://www.google.com")

if __name__ == "__main__":
    open_firefox()
