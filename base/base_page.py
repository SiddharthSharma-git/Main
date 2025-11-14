"""
Base Page Module
Contains common methods for all page objects
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, Optional
from util.logger import Logger


class BasePage:
    """Base class for all page objects with common functionality"""
    
    def __init__(self, driver):
        """
        Initialize base page
        
        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = Logger.get_logger(self.__class__.__name__)
    
    def find_element(self, locator: Tuple[str, str], timeout: int = 20):
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Wait timeout in seconds
            
        Returns:
            WebElement: Found element
        """
        try:
            self.logger.debug(f"Finding element: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = 20):
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Wait timeout in seconds
            
        Returns:
            List of WebElements
        """
        try:
            self.logger.debug(f"Finding elements: {locator}")
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            raise
    
    def click(self, locator: Tuple[str, str]):
        """
        Click on element
        
        Args:
            locator: Tuple of (By strategy, locator value)
        """
        self.logger.info(f"Clicking on element: {locator}")
        element = self.find_element(locator)
        element.click()
    
    def send_keys(self, locator: Tuple[str, str], text: str):
        """
        Send keys to element
        
        Args:
            locator: Tuple of (By strategy, locator value)
            text: Text to send
        """
        self.logger.info(f"Sending keys to element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get text from element
        
        Args:
            locator: Tuple of (By strategy, locator value)
            
        Returns:
            str: Element text
        """
        self.logger.info(f"Getting text from element: {locator}")
        element = self.find_element(locator)
        return element.text
    
    def is_element_displayed(self, locator: Tuple[str, str], timeout: int = 10) -> bool:
        """
        Check if element is displayed
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if displayed, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = 20):
        """
        Wait for element to be clickable
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Wait timeout in seconds
            
        Returns:
            WebElement: Clickable element
        """
        self.logger.debug(f"Waiting for element to be clickable: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def scroll_to_element(self, locator: Tuple[str, str]):
        """
        Scroll to element (Android/iOS compatible)
        
        Args:
            locator: Tuple of (By strategy, locator value)
        """
        self.logger.info(f"Scrolling to element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("mobile: scrollToElement", {"element": element})
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 800):
        """
        Perform swipe gesture
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Swipe duration in milliseconds
        """
        self.logger.info(f"Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    
    def hide_keyboard(self):
        """Hide mobile keyboard if visible"""
        try:
            self.logger.info("Hiding keyboard")
            self.driver.hide_keyboard()
        except Exception as e:
            self.logger.debug(f"Keyboard not visible or unable to hide: {str(e)}")
    
    def take_screenshot(self, filename: str):
        """
        Take screenshot
        
        Args:
            filename: Screenshot filename
        """
        self.logger.info(f"Taking screenshot: {filename}")
        self.driver.save_screenshot(filename)

