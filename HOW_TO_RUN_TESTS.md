# 🚀 How to Run Mumzworld Mobile Tests

## ✅ Pre-Execution Checks (Automatic)

The test framework now automatically checks:
1. ✓ **Device/Emulator** is connected
2. ✓ **Appium Server** is running
3. ✓ **Application** is installed
4. ✓ **App Launch** before tests

---

## 📋 Three Ways to Execute Tests

### **Option 1: Super Easy - Automated Check & Run (RECOMMENDED)** 🌟

This is the **EASIEST** way - it checks everything and even offers to start Appium/emulator if needed!

```bash
cd /Users/sunilkumarmahakur/Documents/appium-mobile-framework

./check_and_run.sh
```

**What it does:**
- ✓ Checks if device is connected (offers to start emulator)
- ✓ Checks if Appium is running (offers to start it)
- ✓ Verifies app is installed
- ✓ Launches the app
- ✓ Runs all test cases
- ✓ Generates HTML report

---

### **Option 2: Using Shell Script with Pre-Checks**

```bash
cd /Users/sunilkumarmahakur/Documents/appium-mobile-framework

./run_tests.sh --platform android
```

**What it checks:**
- ✓ Appium server running
- ✓ Device connected
- ✓ App installed
- ✓ Launches app automatically
- ✓ Runs tests

**Additional Options:**
```bash
# Run smoke tests only
./run_tests.sh --platform android --marker smoke

# Run with HTML report
./run_tests.sh --platform android --report html

# Run with Allure report
./run_tests.sh --platform android --report allure
```

---

### **Option 3: Direct Pytest Command**

For more control, use pytest directly:

```bash
cd /Users/sunilkumarmahakur/Documents/appium-mobile-framework

# Run all tests
python3 -m pytest tests/test_mumzworld.py --platform=android -v --html=test_reports/report.html --self-contained-html

# Run only login test
python3 -m pytest tests/test_mumzworld.py::TestMumzworld::test_successful_login --platform=android -v

# Run only add to cart test
python3 -m pytest tests/test_mumzworld.py::TestMumzworld::test_successful_add_to_cart --platform=android -v
```

---

## 🔧 Manual Setup (If Needed)

If you want to do everything manually:

### 1. Start Appium Server
```bash
appium
```

### 2. Start Emulator (if needed)
```bash
emulator -avd Pixel_5_API_30
```

### 3. Check Device Connection
```bash
adb devices
```

### 4. Install App (if not installed)
```bash
adb install path/to/mumzworld.apk
```

### 5. Launch App
```bash
adb shell am start -n com.mumzworld.android/com.mumzworld.android.MainActivity
```

### 6. Run Tests
```bash
python3 -m pytest tests/test_mumzworld.py --platform=android -v
```

---

## 📊 After Test Execution

### View Reports

**HTML Report:**
```bash
open test_reports/report.html
```

**Screenshots (on failure):**
```bash
open test_reports/screenshots/
```

**Allure Report (if generated):**
```bash
allure serve test_reports/allure_results
```

---

## 🎯 Test Execution Examples

### Run Specific Tests

```bash
# Run by marker
python3 -m pytest tests/ -m smoke --platform=android -v
python3 -m pytest tests/ -m login --platform=android -v
python3 -m pytest tests/ -m cart --platform=android -v

# Run with live logs
python3 -m pytest tests/test_mumzworld.py --platform=android -v -s

# Stop on first failure
python3 -m pytest tests/test_mumzworld.py --platform=android -v -x

# Run in parallel (2 threads)
python3 -m pytest tests/test_mumzworld.py --platform=android -v -n 2
```

---

## 🐛 Troubleshooting

### Issue: "No device connected"
**Solution:**
```bash
# Check devices
adb devices

# Restart ADB
adb kill-server
adb start-server

# Start emulator
emulator -avd Pixel_5_API_30
```

### Issue: "App not installed"
**Solution:**
```bash
# Check if app is installed
adb shell pm list packages | grep mumzworld

# Install app
adb install path/to/mumzworld.apk
```

### Issue: "Appium not running"
**Solution:**
```bash
# Start Appium
appium

# Or with specific port
appium -p 4723
```

### Issue: "Tests fail to find elements"
**Solution:**
- Check if app is already open
- Verify locators in page objects
- Use Appium Inspector to find correct locators

---

## 📱 Quick Commands Reference

```bash
# Check everything is ready
adb devices                                    # Check device
curl http://localhost:4723/status              # Check Appium
adb shell pm list packages | grep mumzworld    # Check app

# Launch app manually
adb shell am start -n com.mumzworld.android/com.mumzworld.android.MainActivity

# Clear app data (fresh start)
adb shell pm clear com.mumzworld.android

# View app logs
adb logcat | grep mumzworld

# Take screenshot manually
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png
```

---

## ✨ Best Practices

1. **Always use `check_and_run.sh`** for hassle-free execution
2. **Check HTML reports** after each run
3. **Review screenshots** when tests fail
4. **Run smoke tests** before full regression
5. **Keep app updated** to latest version

---

## 📞 Support

If you encounter any issues:
1. Check the logs in terminal output
2. View HTML report: `test_reports/report.html`
3. Check screenshots: `test_reports/screenshots/`
4. Review Appium logs

---

**Happy Testing! 🎉**

