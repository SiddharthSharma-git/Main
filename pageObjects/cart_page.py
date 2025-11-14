"""
Cart Page Object
Contains locators and methods for Shopping Cart
"""
from base.base_page import BasePage
from selenium.webdriver.common.by import By
from util.logger import Logger


logger = Logger.get_logger(__name__)


class CartPage(BasePage):
    """Cart Page Object Class"""
    
    # Cart Locators - Based on actual app source
    CART_TAB = (By.XPATH, "//android.widget.Button[@content-desc='Cart']")
    CART_ITEM = (By.ID, "com.mumzworld.android:id/cart_item")
    CART_ITEM_NAME = (By.ID, "com.mumzworld.android:id/cart_item_name")
    CART_ITEM_PRICE = (By.ID, "com.mumzworld.android:id/cart_item_price")
    CART_ITEM_QUANTITY = (By.ID, "com.mumzworld.android:id/cart_item_quantity")
    EMPTY_CART_MESSAGE = (By.XPATH, "//android.widget.TextView[contains(@text,'empty') or contains(@text,'Empty')]")
    CART_BADGE = (By.ID, "com.mumzworld.android:id/cart_badge")
    
    # Checkout
    CHECKOUT_BUTTON = (By.ID, "com.mumzworld.android:id/btnCheckout")
    
    def __init__(self, driver):
        """Initialize Cart Page"""
        super().__init__(driver)
        logger.info("Cart Page initialized")
    
    def click_cart_tab(self):
        """Click on cart tab in bottom navigation"""
        logger.info("Clicking on cart tab")
        self.click(self.CART_TAB)
    
    def is_cart_page_displayed(self):
        """
        Verify if cart page is displayed
        
        Returns:
            bool: True if cart page is displayed
        """
        logger.info("Verifying cart page is displayed")
        return self.is_element_displayed(self.CHECKOUT_BUTTON) or \
               self.is_element_displayed(self.CART_ITEM)
    
    def is_item_in_cart(self):
        """
        Verify if any item is present in cart
        
        Returns:
            bool: True if item is in cart
        """
        logger.info("Checking if item is present in cart")
        try:
            # Check if cart item is displayed
            if self.is_element_displayed(self.CART_ITEM):
                return True
            # Check if empty cart message is NOT displayed
            return not self.is_element_displayed(self.EMPTY_CART_MESSAGE)
        except:
            return False
    
    def get_cart_item_name(self):
        """
        Get name of first item in cart
        
        Returns:
            str: Cart item name
        """
        logger.info("Getting cart item name")
        return self.get_text(self.CART_ITEM_NAME)
    
    def get_cart_items_count(self):
        """
        Get number of items in cart
        
        Returns:
            int: Number of items in cart
        """
        logger.info("Getting cart items count")
        try:
            items = self.driver.find_elements(*self.CART_ITEM)
            return len(items)
        except:
            return 0
    
    def is_cart_badge_displayed(self):
        """
        Verify if cart badge (item count) is displayed
        
        Returns:
            bool: True if cart badge is displayed
        """
        logger.info("Checking if cart badge is displayed")
        return self.is_element_displayed(self.CART_BADGE)
    
    def get_cart_badge_count(self):
        """
        Get cart badge count
        
        Returns:
            str: Cart badge count
        """
        logger.info("Getting cart badge count")
        return self.get_text(self.CART_BADGE)

