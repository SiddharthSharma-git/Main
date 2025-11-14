#!/bin/bash

# Mobile Automation Test Execution Script

echo "========================================"
echo "Mobile Automation Test Execution"
echo "========================================"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
PLATFORM="android"
MARKER="all"
WORKERS=1
REPORT_TYPE="html"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --platform)
      PLATFORM="$2"
      shift 2
      ;;
    --marker)
      MARKER="$2"
      shift 2
      ;;
    --workers)
      WORKERS="$2"
      shift 2
      ;;
    --report)
      REPORT_TYPE="$2"
      shift 2
      ;;
    --help)
      echo "Usage: ./run_tests.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --platform <android|ios>    Mobile platform (default: android)"
      echo "  --marker <marker>           Test marker (smoke, regression, all)"
      echo "  --workers <number>          Number of parallel workers (default: 1)"
      echo "  --report <html|allure>      Report type (default: html)"
      echo "  --help                      Show this help message"
      echo ""
      echo "Examples:"
      echo "  ./run_tests.sh --platform android --marker smoke"
      echo "  ./run_tests.sh --platform ios --workers 3 --report allure"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Check if Appium is running
echo -e "${YELLOW}Checking Appium server...${NC}"
if curl -s http://localhost:4723/status > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Appium server is running${NC}"
else
    echo -e "${RED}✗ Appium server is not running${NC}"
    echo -e "${YELLOW}Please start Appium server: appium${NC}"
    exit 1
fi

# Check if device is connected
echo -e "${YELLOW}Checking for connected devices...${NC}"
DEVICE_COUNT=$(adb devices | grep -w "device" | wc -l)
if [ $DEVICE_COUNT -eq 0 ]; then
    echo -e "${RED}✗ No Android device/emulator connected${NC}"
    echo -e "${YELLOW}Please connect a device or start an emulator${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Device connected${NC}"
fi

# Check if app is installed
APP_PACKAGE="com.mumzworld.android"
echo -e "${YELLOW}Checking if $APP_PACKAGE is installed...${NC}"
if adb shell pm list packages | grep -q "$APP_PACKAGE"; then
    echo -e "${GREEN}✓ Application is installed${NC}"
    
    # Try to launch the app
    echo -e "${YELLOW}Launching application...${NC}"
    adb shell am start -n "$APP_PACKAGE/com.mumzworld.android.MainActivity" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Application launched successfully${NC}"
        sleep 3  # Wait for app to fully load
    else
        echo -e "${YELLOW}⚠ Could not launch app, but will proceed with tests${NC}"
    fi
else
    echo -e "${RED}✗ Application $APP_PACKAGE is not installed${NC}"
    echo -e "${YELLOW}Please install the application first${NC}"
    exit 1
fi

# Build pytest command
PYTEST_CMD="pytest tests/"

if [ "$MARKER" != "all" ]; then
    PYTEST_CMD="$PYTEST_CMD -m $MARKER"
fi

PYTEST_CMD="$PYTEST_CMD --platform=$PLATFORM -v"

if [ "$WORKERS" -gt 1 ]; then
    PYTEST_CMD="$PYTEST_CMD -n $WORKERS"
fi

if [ "$REPORT_TYPE" == "html" ]; then
    PYTEST_CMD="$PYTEST_CMD --html=test_reports/report.html --self-contained-html"
elif [ "$REPORT_TYPE" == "allure" ]; then
    PYTEST_CMD="$PYTEST_CMD --alluredir=test_reports/allure_results"
fi

# Display configuration
echo ""
echo "Test Configuration:"
echo "  Platform: $PLATFORM"
echo "  Marker: $MARKER"
echo "  Workers: $WORKERS"
echo "  Report Type: $REPORT_TYPE"
echo ""

# Run tests
echo -e "${YELLOW}Starting test execution...${NC}"
echo "Command: $PYTEST_CMD"
echo "========================================"

eval $PYTEST_CMD
TEST_EXIT_CODE=$?

echo "========================================"

# Check test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed!${NC}"
fi

# Generate Allure report if requested
if [ "$REPORT_TYPE" == "allure" ]; then
    echo ""
    echo -e "${YELLOW}Generating Allure report...${NC}"
    allure serve test_reports/allure_results
fi

echo ""
echo "Test execution completed!"
echo "Check reports in: test_reports/"

exit $TEST_EXIT_CODE

