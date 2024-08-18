please download https://github.com/yoyo-da/barco_test_annie.
for quiz1, please check 1_test plan.docx
for quiz2, please check test_scripts
for quize3, please check 3_issue.docx
2_readme.ini is for test scripts executions, I have copied details here, so that you could have preview.
README: Warranty Lookup Automation Script
1. Project Overview
This project automates the process of checking product warranty information using Selenium WebDriver and pytest. 
The script supports multiple browsers(chrome/firefox/edge), automatically handles cookie consent pop-ups, enters a serial number, and retrieves warranty details for validation.

2. Main Files
warranty_actions.py: Contains the WarrantyActions class, which handles all actions related to warranty lookup.
test_warranty.py: Contains the TestWarrantyPage class, which uses pytest to test different browser and serial number combinations.
3. Installation
Clone the Repository: git clone https://github.com/yoyo-da/barco_test_annie/tree/main or download the zip file directly.
cd test_test_script
It's recommended to create a virtual environment:
python3 -m venv venv
venv\Scripts\activate    for windows
pip install -r requirements.txt

install requirements:
pip install selenium
pip install pytest pytest-html
Download WebDriver compatible with your version(check your browser version and download closest webdriver version):
ChromeDriver(chrome): https://googlechromelabs.github.io/chrome-for-testing
GeckoDriver (Firefox): https://github.com/mozilla/geckodriver/releases
EdgeDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH
Ensure the WebDriver executable is available in your system's PATH or put WebDriver under test_scripts directory.
If you only want to test on chrome, please make sure pytest.mark.parametriz value updated.
for example: Chrome: 127.0.6533.120, WebdriverVersion: 127.0.6533.119-win64
             Firefox: 115.14.0esr, WebdriverVersion:v0.35.0-win64
             Edge: 127.0.2651.105, WebdriverVersion:127.0.2651.105-x64


4. Usage
Configure Test Parameters
In test_warranty.py:
URL = "https://www.barco.com/en/support/clickshare-extended-warranty/warranty"
Update the pytest.mark.parametrize decorator to test different browser and serial number combinations:
if you only want to test chrome, you could comment/delete other configs:
@pytest.mark.parametrize("browser, serial_number", [
    ("chrome", "1863552437"),
   #("firefox", "1863552437"),
   #("edge", "1863552437"),
   #("browser-name","serial_number")		#you could use other combination
])
5. Run the Tests

Run the tests using pytest:  pytest -v -s --html=report.html --self-contained-html --capture=tee-sys will generate report.html under test_scripts
or execute it on pycharm by right click run Pytests you could see log print on console

The script will:
a. Launch the specified browser: https://www.barco.com/en/support/clickshare-extended-warranty/warranty.
b. Navigate to the warranty lookup page.
c. Handle the cookie consent pop-up if it appears.
d. Enter the provided serial number and click the "Get Info" button.
e. Retrieve and validate the warranty information.
f. View Logs

6. Troubleshooting
WebDriver Not Found: Ensure the correct WebDriver is installed and available in the PATH.
Timeout Issues: If elements take longer to load, consider increasing the timeout duration in WebDriverWait.
Browser-Specific Issues: Different browsers may behave differently, especially in handling JavaScript or loading elements.

7. Contact
For any issues or suggestions, please contact nswd0608@outlook.com
