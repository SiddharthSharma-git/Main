# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Prerequisites

```bash
# Install Python dependencies
cd ~/Documents/appium-mobile-framework
python -m venv venv
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
```

### Step 2: Install Appium (if not already installed)

```bash
# Install Appium globally
npm install -g appium

# Install drivers
appium driver install uiautomator2  # For Android
appium driver install xcuitest       # For iOS
```

### Step 3: Configure Your App

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your app details
# Update these values:
# - ANDROID_APP_PATH or IOS_APP_PATH
# - APP_PACKAGE and APP_ACTIVITY (for Android)
# - BUNDLE_ID (for iOS)
```

### Step 4: Update Page Locators

Since this is a template, you need to update the locators in page objects to match your app:

**Edit `pageObjects/login_page.py`:**
```python
# Update these locators with your app's actual element IDs
USERNAME_FIELD = (AppiumBy.ID, "your_actual_username_id")
PASSWORD_FIELD = (AppiumBy.ID, "your_actual_password_id")
LOGIN_BUTTON = (AppiumBy.ID, "your_actual_login_button_id")
```

**Edit `pageObjects/home_page.py`:**
```python
# Update these locators with your app's actual element IDs
WELCOME_MESSAGE = (AppiumBy.ID, "your_actual_welcome_id")
# ... and other locators
```

### Step 5: Start Appium Server

```bash
# In a separate terminal window
appium
```

### Step 6: Connect Your Device/Emulator

**For Android:**
```bash
# Start Android emulator or connect real device
adb devices  # Verify device is connected
```

**For iOS:**
```bash
# Open iOS Simulator or connect real device
xcrun simctl list  # List available simulators
```

### Step 7: Run Your Tests

```bash
# Run all tests
pytest tests/ --platform=android

# Or use the test runner script
./run_tests.sh --platform android --marker smoke

# Run specific test file
pytest tests/test_login.py -v
```

## 📝 Customizing the Framework

### Adding New Page Objects

1. Create a new file in `pageObjects/` directory:

```python
# pageObjects/settings_page.py
from appium.webdriver.common.appiumby import AppiumBy
from base.base_page import BasePage

class SettingsPage(BasePage):
    
    # Define your locators
    SETTINGS_TITLE = (AppiumBy.ID, "settings_title")
    LOGOUT_BUTTON = (AppiumBy.ID, "logout_button")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_logout(self):
        self.click(self.LOGOUT_BUTTON)
```

2. Create corresponding test file in `tests/`:

```python
# tests/test_settings.py
import pytest
from pageObjects.settings_page import SettingsPage

class TestSettings:
    
    @pytest.mark.regression
    def test_logout(self, driver):
        settings_page = SettingsPage(driver)
        settings_page.click_logout()
        # Add assertions
```

### Finding Element Locators

**Using Appium Inspector:**

1. Download Appium Inspector from: https://github.com/appium/appium-inspector/releases
2. Start your Appium server
3. Connect Appium Inspector with these capabilities:
   ```json
   {
     "platformName": "Android",
     "deviceName": "emulator-5554",
     "app": "/path/to/your/app.apk"
   }
   ```
4. Inspect elements and copy their locators

**Using UIAutomator Viewer (Android):**
```bash
uiautomatorviewer
```

**Using Xcode Accessibility Inspector (iOS):**
Open Xcode → Developer Tools → Accessibility Inspector

## 🎯 Common Test Scenarios

### Test Case 1: Login Flow
```python
def test_login_flow(self, driver):
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    login_page.login("user@example.com", "password123")
    assert home_page.is_home_page_displayed()
```

### Test Case 2: Search Functionality
```python
def test_search(self, driver):
    home_page = HomePage(driver)
    
    home_page.enter_search_text("test query")
    # Add verification
```

### Test Case 3: Data-Driven Tests
```python
@pytest.mark.parametrize("username,password", [
    ("user1@test.com", "pass1"),
    ("user2@test.com", "pass2"),
])
def test_login_multiple_users(self, driver, username, password):
    login_page = LoginPage(driver)
    login_page.login(username, password)
```

## 📊 Viewing Reports

### HTML Report
```bash
pytest --html=test_reports/report.html --self-contained-html
open test_reports/report.html  # Mac
```

### Allure Report
```bash
pytest --alluredir=test_reports/allure_results
allure serve test_reports/allure_results
```

## 🐛 Troubleshooting

### Issue: "Could not find element"
**Solution:** Update locators in page objects to match your app

### Issue: "Connection refused to Appium server"
**Solution:** Make sure Appium server is running on port 4723

### Issue: "No devices found"
**Solution:** 
- For Android: Run `adb devices`
- For iOS: Check iOS Simulator or connected device

### Issue: "App not found"
**Solution:** Update APP_PATH in .env file with correct path

## 📚 Next Steps

1. Update locators for your actual mobile application
2. Add more page objects for different screens
3. Write test cases covering your app's functionality
4. Set up CI/CD integration
5. Configure test data management
6. Add more utility functions as needed

## 💡 Tips

- Always use explicit waits instead of `time.sleep()`
- Keep page objects focused on a single screen/component
- Use descriptive names for test methods
- Add proper logging for debugging
- Take advantage of pytest markers for test organization
- Run smoke tests frequently, regression tests before releases

---

**Happy Testing! 🎉**

