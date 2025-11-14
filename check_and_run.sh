#!/bin/bash

# Comprehensive Mobile Test Execution Script
# Checks environment, app installation, and runs tests

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

APP_PACKAGE="com.mumzworld.android"
APP_ACTIVITY="com.mumzworld.android.MainActivity"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Mumzworld Mobile Test Automation${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to check and start emulator if needed
check_device() {
    echo -e "${YELLOW}Step 1: Checking for connected devices...${NC}"
    DEVICE_COUNT=$(adb devices | grep -w "device" | wc -l)
    
    if [ $DEVICE_COUNT -eq 0 ]; then
        echo -e "${RED}✗ No device/emulator found${NC}"
        echo -e "${YELLOW}Would you like to start an emulator? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo -e "${YELLOW}Starting emulator...${NC}"
            emulator -avd Pixel_5_API_30 &
            sleep 10
            adb wait-for-device
            echo -e "${GREEN}✓ Emulator started${NC}"
        else
            echo -e "${RED}Cannot proceed without a device. Exiting...${NC}"
            exit 1
        fi
    else
        DEVICE_ID=$(adb devices | grep -w "device" | head -1 | awk '{print $1}')
        echo -e "${GREEN}✓ Device connected: $DEVICE_ID${NC}"
    fi
}

# Function to check Appium server
check_appium() {
    echo ""
    echo -e "${YELLOW}Step 2: Checking Appium server...${NC}"
    if curl -s http://localhost:4723/status > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Appium server is running${NC}"
    else
        echo -e "${RED}✗ Appium server is not running${NC}"
        echo -e "${YELLOW}Would you like to start Appium? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo -e "${YELLOW}Starting Appium server...${NC}"
            appium &
            sleep 5
            echo -e "${GREEN}✓ Appium server started${NC}"
        else
            echo -e "${RED}Cannot proceed without Appium. Exiting...${NC}"
            exit 1
        fi
    fi
}

# Function to check app installation
check_app_installation() {
    echo ""
    echo -e "${YELLOW}Step 3: Checking application installation...${NC}"
    
    if adb shell pm list packages | grep -q "$APP_PACKAGE"; then
        echo -e "${GREEN}✓ Application $APP_PACKAGE is installed${NC}"
        
        # Get app version
        VERSION=$(adb shell dumpsys package $APP_PACKAGE | grep versionName | head -1 | awk '{print $1}')
        echo -e "${BLUE}  Version: $VERSION${NC}"
        
        return 0
    else
        echo -e "${RED}✗ Application $APP_PACKAGE is NOT installed${NC}"
        echo -e "${YELLOW}Please install the app first using:${NC}"
        echo -e "${BLUE}  adb install path/to/app.apk${NC}"
        exit 1
    fi
}

# Function to launch app
launch_app() {
    echo ""
    echo -e "${YELLOW}Step 4: Launching application...${NC}"
    
    # Clear app data for fresh start (optional)
    # adb shell pm clear $APP_PACKAGE
    
    # Launch the app
    adb shell am start -n "$APP_PACKAGE/$APP_ACTIVITY" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Application launched successfully${NC}"
        echo -e "${YELLOW}Waiting for app to initialize...${NC}"
        sleep 5
        
        # Verify app is in foreground
        CURRENT_APP=$(adb shell dumpsys window windows | grep -E 'mCurrentFocus' | cut -d'/' -f1 | rev | cut -d' ' -f1 | rev)
        if [[ "$CURRENT_APP" == *"$APP_PACKAGE"* ]]; then
            echo -e "${GREEN}✓ App is in foreground and ready${NC}"
        else
            echo -e "${YELLOW}⚠ App may not be in foreground${NC}"
        fi
    else
        echo -e "${RED}✗ Failed to launch application${NC}"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${YELLOW}Step 5: Running test cases...${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    
    # Run pytest
    python3 -m pytest tests/test_mumzworld.py \
        --platform=android \
        -v \
        --html=test_reports/report.html \
        --self-contained-html
    
    TEST_EXIT_CODE=$?
    
    echo ""
    echo -e "${BLUE}================================================${NC}"
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✓ All tests PASSED!${NC}"
    else
        echo -e "${RED}✗ Some tests FAILED!${NC}"
        echo -e "${YELLOW}Check reports at: test_reports/report.html${NC}"
        echo -e "${YELLOW}Screenshots at: test_reports/screenshots/${NC}"
    fi
    echo -e "${BLUE}================================================${NC}"
    
    return $TEST_EXIT_CODE
}

# Main execution flow
main() {
    check_device
    check_appium
    check_app_installation
    launch_app
    run_tests
    
    EXIT_CODE=$?
    
    echo ""
    echo -e "${BLUE}Test execution completed!${NC}"
    echo -e "${YELLOW}View HTML report:${NC} open test_reports/report.html"
    
    exit $EXIT_CODE
}

# Run main function
main

