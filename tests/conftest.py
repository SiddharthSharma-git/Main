"""
Pytest Configuration File
Contains fixtures and hooks for test execution
"""
import pytest
import pytest_html
import os
from datetime import datetime
from base.driver_factory import DriverFactory
from reports.report_generator import ReportGenerator
from util.logger import Logger


logger = Logger.get_logger(__name__)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Mobile platform: android or ios"
    )
    parser.addoption(
        "--app",
        action="store",
        default="",
        help="Path to mobile application"
    )


@pytest.fixture(scope="session")
def platform(request):
    """Get platform from command line"""
    return request.config.getoption("--platform")


@pytest.fixture(scope="function")
def driver(platform):
    """
    Setup and teardown driver for each test
    
    Args:
        platform: Mobile platform (android/ios)
        
    Yields:
        WebDriver: Appium driver instance
    """
    logger.info("Setting up driver for test")
    driver = DriverFactory.get_driver(platform)
    
    yield driver
    
    logger.info("Tearing down driver after test")
    DriverFactory.quit_driver()


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before all tests"""
    import subprocess
    
    logger.info("=" * 80)
    logger.info("PRE-TEST ENVIRONMENT SETUP")
    logger.info("=" * 80)
    
    # Check if device is connected
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if 'device' not in result.stdout:
            logger.error("No Android device/emulator connected")
            pytest.exit("No device connected. Please connect a device or start emulator.")
        logger.info("✓ Device is connected")
    except Exception as e:
        logger.warning(f"Could not check device status: {str(e)}")
    
    # Check if app is installed
    app_package = "com.mumzworld.android"
    try:
        result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages'], 
                              capture_output=True, text=True)
        if app_package in result.stdout:
            logger.info(f"✓ Application {app_package} is installed")
            
            # Try to launch the app
            logger.info("Launching application...")
            subprocess.run(['adb', 'shell', 'am', 'start', '-n', 
                          f'{app_package}/com.mumzworld.android.MainActivity'],
                         capture_output=True)
            logger.info("✓ Application launched")
            import time
            time.sleep(3)  # Wait for app to load
        else:
            logger.error(f"Application {app_package} is not installed")
            pytest.exit(f"App not installed. Please install {app_package} first.")
    except Exception as e:
        logger.warning(f"Could not check/launch app: {str(e)}")
    
    logger.info("=" * 80)
    logger.info("STARTING TEST EXECUTION")
    logger.info("=" * 80)
    
    yield
    
    logger.info("=" * 80)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info("=" * 80)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only process actual test execution (not setup/teardown)
    if report.when == "call":
        if report.failed:
            logger.error(f"Test FAILED: {item.name}")
            
            # Take screenshot on failure
            try:
                driver = item.funcargs.get('driver')
                if driver:
                    screenshot_dir = os.path.join(
                        os.path.dirname(os.path.dirname(__file__)),
                        "test_reports",
                        "screenshots"
                    )
                    os.makedirs(screenshot_dir, exist_ok=True)
                    
                    screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                    
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot saved: {screenshot_path}")
                    
                    # Attach screenshot to pytest-html report
                    if hasattr(report, 'extra'):
                        report.extra.append(pytest_html.extras.png(screenshot_path))
            except Exception as e:
                logger.error(f"Failed to take screenshot: {str(e)}")
        
        elif report.passed:
            logger.info(f"Test PASSED: {item.name}")


@pytest.fixture(scope="session", autouse=True)
def configure_html_report():
    """Configure HTML report settings"""
    report_gen = ReportGenerator()
    return report_gen.get_html_report_path()


# Pytest HTML report customization
def pytest_configure(config):
    """Configure pytest settings"""
    config._metadata = {
        'Platform': config.getoption('--platform'),
        'Python Version': '3.x',
        'Framework': 'Appium + Pytest'
    }


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Mobile Automation Test Report"

