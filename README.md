# Mobile Automation Framework - Appium with Pytest

A robust and scalable Python-based mobile automation framework using Appium and Pytest for iOS and Android mobile applications.

## 📁 Framework Structure

```
appium-mobile-framework/
├── base/                      # Core framework classes
│   ├── __init__.py
│   ├── driver_factory.py      # Appium driver initialization
│   └── base_page.py           # Base page object with common methods
├── pageObjects/               # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py          # Login page object
│   └── home_page.py           # Home page object
├── tests/                     # Test cases
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and hooks
│   ├── test_login.py          # Login test cases
│   └── test_home.py           # Home page test cases
├── util/                      # Utility classes
│   ├── __init__.py
│   ├── logger.py              # Logging utility
│   └── common_utils.py        # Common helper functions
├── reports/                   # Report generation
│   ├── __init__.py
│   └── report_generator.py   # Report generation utilities
├── config/                    # Configuration files
│   ├── __init__.py
│   └── config.yaml            # Framework configuration
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## 🚀 Features

- **Page Object Model (POM)**: Clean separation of test logic and page elements
- **Dual Platform Support**: Works with both Android and iOS applications
- **Pytest Framework**: Powerful testing framework with fixtures and markers
- **Comprehensive Logging**: Colored console logs and detailed file logs
- **Multiple Report Formats**: HTML reports (pytest-html) and Allure reports
- **Screenshot on Failure**: Automatic screenshot capture when tests fail
- **Parallel Execution**: Support for parallel test execution with pytest-xdist
- **Configurable**: Easy configuration through YAML and environment variables

## 📋 Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Node.js and npm** (for Appium)
   ```bash
   node --version
   npm --version
   ```

3. **Appium Server**
   ```bash
   npm install -g appium
   appium --version
   ```

4. **Appium Drivers**
   ```bash
   # For Android
   appium driver install uiautomator2
   
   # For iOS
   appium driver install xcuitest
   ```

5. **Android SDK** (for Android testing)
   - Android Studio with SDK tools
   - Set ANDROID_HOME environment variable

6. **Xcode** (for iOS testing - Mac only)
   - Xcode with Command Line Tools
   - iOS Simulator or real device

## 🛠️ Installation

1. **Clone or navigate to the framework directory**
   ```bash
   cd ~/Documents/appium-mobile-framework
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Start Appium server**
   ```bash
   appium
   ```

## ⚙️ Configuration

### Environment Variables (.env)

Update the `.env` file with your device and app details:

```env
APPIUM_SERVER_URL=http://localhost:4723
ANDROID_DEVICE_NAME=emulator-5554
ANDROID_APP_PATH=/path/to/your/app.apk
APP_PACKAGE=com.yourapp.package
APP_ACTIVITY=.MainActivity
```

### Config File (config/config.yaml)

Modify `config.yaml` for framework-wide settings.

## 🧪 Running Tests

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_login.py
```

### Run with specific marker
```bash
# Run smoke tests only
pytest -m smoke

# Run regression tests only
pytest -m regression
```

### Run with platform specification
```bash
# Android
pytest --platform=android

# iOS
pytest --platform=ios
```

### Generate HTML report
```bash
pytest --html=test_reports/report.html --self-contained-html
```

### Generate Allure report
```bash
# Run tests and generate results
pytest --alluredir=test_reports/allure_results

# Generate and open report
allure serve test_reports/allure_results
```

### Parallel execution
```bash
pytest -n 3  # Run with 3 parallel workers
```

### Verbose output
```bash
pytest -v -s
```

## 📝 Writing Tests

### Example Test Case

```python
import pytest
import allure
from pageObjects.login_page import LoginPage

@allure.feature('Authentication')
class TestLogin:
    
    @pytest.mark.smoke
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login("user@example.com", "password")
        assert login_page.is_login_successful()
```

### Creating Page Objects

```python
from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class NewPage(BasePage):
    
    # Define locators
    BUTTON = (AppiumBy.ID, "button_id")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_button(self):
        self.click(self.BUTTON)
```

## 📊 Reports

### Test Reports Location
- HTML Reports: `test_reports/report.html`
- Allure Results: `test_reports/allure_results/`
- Screenshots: `test_reports/screenshots/`
- Logs: `logs/`

## 🏷️ Test Markers

- `@pytest.mark.smoke` - Smoke test cases
- `@pytest.mark.regression` - Regression test cases
- `@pytest.mark.android` - Android specific tests
- `@pytest.mark.ios` - iOS specific tests

## 🐛 Debugging

1. **Check Appium server logs** - Appium console output
2. **Review test logs** - Check `logs/` directory
3. **Screenshots** - Automatically captured on test failure
4. **Verbose mode** - Run with `-v -s` flags

## 📚 Best Practices

1. Follow Page Object Model pattern
2. Use explicit waits instead of sleep()
3. Keep test data separate from test logic
4. Use descriptive test and method names
5. Add proper logging and assertions
6. Handle exceptions appropriately
7. Clean up resources in teardown

## 🤝 Contributing

1. Create page objects for new screens
2. Write test cases with proper markers
3. Update documentation
4. Follow coding standards

## 📄 License

This framework is created for educational and testing purposes.

## 👥 Author

Created as a mobile automation framework template.

## 📞 Support

For issues and questions:
- Check logs in `logs/` directory
- Review Appium server console
- Verify device/emulator connectivity
- Ensure app paths are correct

---

**Happy Testing! 🚀**

