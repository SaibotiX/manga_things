from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def open_firefox():
    """Open Firefox and navigate to google.com."""
    options = Options()
  #  options.add_argument('--no-sandbox')
   # options.add_argument('--disable-dev-shm-usage')
    
    service = Service(executable_path="/snap/bin/geckodriver") # specify the path to your geckodriver
    driver = webdriver.Firefox(options=options, service=service)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.get("https://www.google.com") # navigate to Google

if __name__ == "__main__":
    open_firefox()
