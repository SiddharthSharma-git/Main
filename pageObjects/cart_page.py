from base.base_page import BasePage
from selenium.webdriver.common.by import By
from util.logger import Logger

logger = Logger.get_logger(__name__)

class CartPage(BasePage):
    CART_TAB = (By.XPATH, "//android.widget.Button[@content-desc='Cart']")
    CART_ITEM = (By.ID, "com.mumzworld.android:id/cart_item")
    CART_ITEM_NAME = (By.ID, "com.mumzworld.android:id/cart_item_name")
    CART_ITEM_PRICE = (By.ID, "com.mumzworld.android:id/cart_item_price")
    CART_ITEM_QUANTITY = (By.ID, "com.mumzworld.android:id/cart_item_quantity")
    EMPTY_CART_MESSAGE = (By.XPATH, "//android.widget.TextView[contains(@text,'empty') or contains(@text,'Empty')]")
    CART_BADGE = (By.ID, "com.mumzworld.android:id/cart_badge")
    
   
    CHECKOUT_BUTTON = (By.ID, "com.mumzworld.android:id/btnCheckout")
    
    def __init__(self, driver):
        
        super().__init__(driver)
        logger.info("Cart Page initialized")
    
    def click_cart_tab(self):
        
        logger.info("Clicking on cart tab")
        self.click(self.CART_TAB)
    
    def is_cart_page_displayed(self):
        
        logger.info("Verifying cart page is displayed")
        return self.is_element_displayed(self.CHECKOUT_BUTTON) or \
               self.is_element_displayed(self.CART_ITEM)
    
    def is_item_in_cart(self):
        
        logger.info("Checking if item is present in cart")
        try:
            
            if self.is_element_displayed(self.CART_ITEM):
                return True
            
            return not self.is_element_displayed(self.EMPTY_CART_MESSAGE)
        except:
            return False
    
    def get_cart_item_name(self):
        
        logger.info("Getting cart item name")
        return self.get_text(self.CART_ITEM_NAME)
    
    def get_cart_items_count(self):
       
        logger.info("Getting cart items count")
        try:
            items = self.driver.find_elements(*self.CART_ITEM)
            return len(items)
        except:
            return 0
    
    def is_cart_badge_displayed(self):
        
        logger.info("Checking if cart badge is displayed")
        return self.is_element_displayed(self.CART_BADGE)
    
    def get_cart_badge_count(self):
        
        logger.info("Getting cart badge count")
        return self.get_text(self.CART_BADGE)

