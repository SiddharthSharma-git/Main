"""
Driver Factory Module
Handles Appium driver initialization and configuration
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from typing import Optional
import os
from util.logger import Logger


class DriverFactory:
    """Factory class to create and manage Appium driver instances"""
    
    _driver: Optional[webdriver.Remote] = None
    logger = Logger.get_logger(__name__)
    
    @classmethod
    def get_driver(cls, platform: str = "android") -> webdriver.Remote:
        """
        Get or create Appium driver instance
        
        Args:
            platform: Mobile platform - 'android' or 'ios'
            
        Returns:
            webdriver.Remote: Appium driver instance
        """
        if cls._driver is None:
            cls._driver = cls._create_driver(platform)
        return cls._driver
    
    @classmethod
    def _create_driver(cls, platform: str) -> webdriver.Remote:
        """
        Create new Appium driver instance
        
        Args:
            platform: Mobile platform - 'android' or 'ios'
            
        Returns:
            webdriver.Remote: New Appium driver instance
        """
        appium_server_url = os.getenv('APPIUM_SERVER_URL', 'http://localhost:4723')
        
        cls.logger.info(f"Initializing {platform} driver...")
        
        if platform.lower() == "android":
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.device_name = os.getenv('ANDROID_DEVICE_NAME', 'emulator-5554')
            options.automation_name = "UiAutomator2"
            options.app = os.getenv('ANDROID_APP_PATH', '')
            options.app_package = os.getenv('APP_PACKAGE', '')
            options.app_activity = os.getenv('APP_ACTIVITY', '')
            options.no_reset = False
            
        elif platform.lower() == "ios":
            options = XCUITestOptions()
            options.platform_name = "iOS"
            options.device_name = os.getenv('IOS_DEVICE_NAME', 'iPhone 14')
            options.automation_name = "XCUITest"
            options.app = os.getenv('IOS_APP_PATH', '')
            options.bundle_id = os.getenv('BUNDLE_ID', '')
            options.no_reset = False
        else:
            raise ValueError(f"Unsupported platform: {platform}")
        
        cls.logger.info(f"Connecting to Appium server at {appium_server_url}")
        driver = webdriver.Remote(appium_server_url, options=options)
        driver.implicitly_wait(10)
        
        cls.logger.info(f"{platform} driver initialized successfully")
        return driver
    
    @classmethod
    def quit_driver(cls):
        """Quit and cleanup driver instance"""
        if cls._driver is not None:
            cls.logger.info("Quitting driver...")
            cls._driver.quit()
            cls._driver = None
            cls.logger.info("Driver quit successfully")

