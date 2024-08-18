import pytest
from warranty_actions import WarrantyActions


class TestWarrantyPage:
    URL = "https://www.barco.com/en/support/clickshare-extended-warranty/warranty"
    TIMEOUT = 10

    @classmethod
    def setup_class(cls):
        """Setup WebDriver and initialize logger."""
        cls.logger = WarrantyActions()._setup_logger()

    @pytest.mark.parametrize("browser, serial_number", [
        ("chrome", "1863552437"),
        ("firefox", "1863552437"),
        ("edge", "1863552437"),
        ("chrome", "dfadfadg"),
        # Add more browser and serial number combinations as needed
    ])
    def test_warranty_lookup(self, browser, serial_number):
        """
        :param browser: str, browser used for test, only support chrome/firefox/edge so far
        :param serial_number: str, serial number for check
        :return: dict, warranty_info for further usage if needed
        Retrieve the warranty information from the result page, support different types browsers
        step: initialize webdriver based on browser--accept cookie if needed--enter serial and click-get warranty info for check
        """
        actions = WarrantyActions(logger=self.logger)
        actions._initialize_webdriver(browser, self.URL)
        try:
            actions.accept_cookies()
            actions.enter_serial_and_click(serial_number)
            if not actions.handle_invalid_serial_number():
                self.logger.warning(f"No warranty info found for serial number {serial_number} on {browser}.")
                return  # Exit the test if the serial number is invalid
            displayed_serial_number, warranty_info = actions.get_warranty_info()
            self.logger.info(f"Displayed serial number: {displayed_serial_number}")
            self.logger.info(f"Warranty results: {warranty_info}")
            if str(displayed_serial_number).strip() != str(serial_number).strip():
                self.logger.warning(f"Error: searched for {serial_number}, but returned {displayed_serial_number}.")
            else:
                print(browser, ":", warranty_info)
                assert 'Warranty end date' in warranty_info
                assert warranty_info['Warranty end date']
                assert displayed_serial_number == serial_number
                return warranty_info
        finally:
            if actions.driver:
                actions.driver.quit()


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_latest_V6.py"])
