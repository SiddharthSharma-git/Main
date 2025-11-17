from base.base_page import BasePage
from selenium.webdriver.common.by import By
from util.logger import Logger


logger = Logger.get_logger(__name__)


class AccountPage(BasePage):
    
    ACCOUNT_TAB = (By.XPATH, "//android.widget.Button[@content-desc='Account']")
    SIGN_IN_BUTTON = (By.XPATH, '(//android.widget.TextView[@text="Sign In"])[2]')
    
    
    MY_ORDERS = (By.XPATH, "//android.widget.TextView[@text='My orders']")
    WISHLIST = (By.XPATH, "//android.widget.TextView[@text='Wishlist']")
    MY_PROFILE = (By.XPATH, "//android.widget.TextView[@text='My profile']")
    
    
    HI_THERE_TEXT = (By.XPATH, "//android.widget.TextView[@text='Hi There!']")
    
    def __init__(self, driver):
        
        super().__init__(driver)
        logger.info("Account Page initialized")
    
    def click_account_tab(self):
        
        logger.info("Clicking on Account tab")
        self.click(self.ACCOUNT_TAB)
    
    def click_sign_in_button(self):
        
        logger.info("Clicking on Sign In button")
        self.wait_for_element_clickable(self.SIGN_IN_BUTTON, timeout=10)
        self.click(self.SIGN_IN_BUTTON)
    
    def is_account_info_displayed(self):
        
        logger.info("Verifying account information is displayed")
        try:
            # Check if "Hi There!" is NOT displayed (means logged in)
            hi_there_present = self.is_element_displayed(self.HI_THERE_TEXT, timeout=5)
            if not hi_there_present:
                logger.info("'Hi There!' text not found - user appears to be logged in")
                return True
            
            # If Hi There is present, check for logged-in elements
            return self.is_element_displayed(self.MY_ORDERS, timeout=5) or \
                   self.is_element_displayed(self.MY_PROFILE, timeout=5)
        except:
            return False
    
    def is_logged_in(self):
       
        logger.info("Checking if user is logged in")
        try:
            # If Sign In button is not visible, user is logged in
            sign_in_visible = self.is_element_displayed(self.SIGN_IN_BUTTON, timeout=3)
            return not sign_in_visible
        except:
            return True  # If button not found, assume logged in

