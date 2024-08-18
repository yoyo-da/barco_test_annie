import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class WarrantyActions:
    """This class provide method for test_warranty"""
    def __init__(self, driver=None, logger=None):
        self.TIMEOUT = 10
        self.driver = driver
        self.waitdriver = WebDriverWait(self.driver, self.TIMEOUT)
        self.logger = logger


    def setup_logger(self):
        """Setup logger configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def initialize_webdriver(self, browser, url):
        """Create and return a WebDriver instance based on the selected browser."""
        if browser == 'chrome':
            chrome_options = ChromeOptions()
            self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
        elif browser == 'firefox':
            firefox_options = FirefoxOptions()
            self.driver = webdriver.Firefox(service=FirefoxService(), options=firefox_options)
        elif browser == 'edge':
            edge_options = EdgeOptions()
            self.driver = webdriver.Edge(service=EdgeService(), options=edge_options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        self.driver.maximize_window()
        self.waitdriver = WebDriverWait(self.driver, self.TIMEOUT)  # Assuming a default timeout of 10 seconds
        self.driver.implicitly_wait(self.TIMEOUT)  # Assuming a default timeout of 10 seconds
        self.driver.get(url)

    def accept_cookies(self):
        """Handle the cookie consent popup."""
        try:
            self.logger.info("Attempting to click the 'Accept Cookies' button.")
            accept_button = self.waitdriver.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
            )
            accept_button.click()
            self.logger.info("'Accept Cookies' button clicked successfully.")
        except:
            self.logger.info(f"No cookie verification needed")

    def enter_serial_and_click(self, serial_number):
        """Enter the serial number and click the 'Get Info' button."""
        try:
            self.logger.info(f"Entering serial number: {serial_number}")
            serial_input = self.driver.find_element(by=By.XPATH, value="//div[@id='warranty']//input[@id='serial']")
            serial_input.clear()  # Clear any existing text
            serial_input.send_keys(serial_number)

            self.logger.info("Clicking the 'Get Info' button.")
            get_info_button = self.driver.find_element(by=By.XPATH, value="//div[@id='warranty']//button[@type='submit']")
            get_info_button.click()
            self.logger.info("Waiting for the warranty info to be displayed.")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def get_warranty_info(self):
        """Retrieve the warranty information from the result page.
        return tuple contains (displayed_serial_number:str, warranty_results:dict)
        step1. check warranty results for serial_number, return None if no ele, retrun serial_number if found
        step2. if found warranty_results, save detailed warranty_results as dict 
        """
        try:
            h5_xpath = "//div[@id='warranty']//h5[@class='mt-8 mb-0']"
            h5_element = self.waitdriver.until(EC.presence_of_element_located((By.XPATH, h5_xpath)))
        except TimeoutException:
            return
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
        displayed_serial_number = h5_element.text.strip().split(" ")[-1]
        dd_elements = self.driver.find_elements(By.XPATH, "//div[@id='warranty']//dl[contains(@class, 'cmp-product-warranty__list')]//dd")
        dt_elements = self.driver.find_elements(By.XPATH, "//div[@id='warranty']//dl[contains(@class, 'cmp-product-warranty__list')]//dt")
        warranty_results = {dt.text: dd.text for dt, dd in zip(dt_elements, dd_elements)}
        self.driver.get_screenshot_as_file("warranty_result.png")
        return displayed_serial_number, warranty_results

    def handle_invalid_serial_number(self):
        """Check if the warranty information is not available.
        step1. get displayed serial_number by get_warranty_info
        step2. if empty, assert warranty info not displayed, then return False
        step3. else if there's serial_number, then return True
        """
        warranty_info = self.get_warranty_info()
        if not warranty_info:
            warrany_list_xpath = "//div[@id='warranty']//dl[contains(@class, 'cmp-product-warranty__list')]"
            elements = self.driver.find_elements(By.XPATH, warrany_list_xpath)
            assert len(elements) == 0
            return False
        return True
