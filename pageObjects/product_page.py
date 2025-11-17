from base.base_page import BasePage
from selenium.webdriver.common.by import By
from util.logger import Logger


logger = Logger.get_logger(__name__)


class ProductPage(BasePage):
    
    EXPLORE_BUTTON = (By.XPATH, '//android.widget.Button[@content-desc="Explore"]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView[5]')
    SEARCH_ICON = (By.XPATH, '//com.horcrux.svg.SvgView[@resource-id="phosphor-react-native-magnifying-glass-bold"]/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')
    SEARCH_FIELD = (By.XPATH, '//android.widget.EditText[@text="Search Mumzworld"]')
    
    
    SEARCH_SUGGESTION_FIRST = (By.XPATH, "(//android.widget.TextView)[1]")
    SEARCH_SUGGESTIONS = (By.XPATH, "//android.widget.TextView")
    
    
    PRODUCT_ITEM = (By.XPATH, "//android.view.ViewGroup[@clickable='true' and @enabled='true']")
    PRODUCT_NAME = (By.XPATH, "//android.widget.TextView")
    
    
    ADD_ICON = (By.XPATH, "//android.widget.ImageView[@content-desc='Add to cart' or contains(@content-desc, 'Add')]")
    PLUS_ICON = (By.XPATH, "//android.view.ViewGroup[contains(@content-desc, 'add') or contains(@content-desc, 'plus')]")
    ADD_BUTTON_GENERIC = (By.XPATH, "//android.widget.Button[contains(@content-desc, 'Add') or @text='+']")
    
    
    PDP_TITLE = (By.ID, "com.mumzworld.android:id/pdp_title")
    PDP_PRICE = (By.ID, "com.mumzworld.android:id/pdp_price")
    ADD_TO_CART_BUTTON = (By.ID, "com.mumzworld.android:id/btnAddToCart")
    ADD_TO_CART_BUTTON_ALT = (By.XPATH, "//android.widget.Button[@text='Add to Cart']")
    QUANTITY_SELECTOR = (By.ID, "com.mumzworld.android:id/quantity_selector")
    
    
    CART_SUCCESS_MESSAGE = (By.XPATH, "//android.widget.TextView[contains(@text,'added to cart')]")
    
    def __init__(self, driver):
        
        super().__init__(driver)
        logger.info("Product Page initialized")
    
    def click_explore_button(self):
        
        logger.info("Clicking on Explore button")
        self.wait_for_element_clickable(self.EXPLORE_BUTTON, timeout=10)
        self.click(self.EXPLORE_BUTTON)
        self.driver.implicitly_wait(2)
    
    def click_search_icon(self):
        
        logger.info("Clicking on search icon")
        self.wait_for_element_clickable(self.SEARCH_ICON, timeout=10)
        self.click(self.SEARCH_ICON)
    
    def enter_search_text(self, search_text):
        
        logger.info(f"Entering search text: {search_text}")
        
        self.click_explore_button()
        
        self.click_search_icon()
       
        self.driver.implicitly_wait(3)
        
        logger.info("Finding search field")
        search_field = self.find_element(self.SEARCH_FIELD, timeout=10)
        search_field.send_keys(search_text)
        
        self.driver.implicitly_wait(2)
    
    def select_first_search_suggestion(self):
       
        logger.info("Selecting first search suggestion from dropdown")
        
        self.driver.implicitly_wait(3)
        try:
            suggestions = self.find_elements(self.SEARCH_SUGGESTIONS, timeout=10)
            if suggestions and len(suggestions) > 0:
                logger.info(f"Found {len(suggestions)} search suggestions")
            
                suggestions[0].click()
                logger.info("Clicked first search suggestion")
                self.driver.implicitly_wait(2)
            else:
                raise Exception("No search suggestions found")
        except Exception as e:
            logger.error(f"Error selecting search suggestion: {str(e)}")
            raise
    
    def click_add_icon(self):
        
        logger.info("Clicking on + icon to add to cart")
        
        self.driver.implicitly_wait(3)
        try:
            
            try:
                logger.info("Trying ADD_ICON locator")
                self.wait_for_element_clickable(self.ADD_ICON, timeout=10)
                self.click(self.ADD_ICON)
                logger.info("Clicked add icon")
            except:
                try:
                    logger.info("Trying PLUS_ICON locator")
                    self.wait_for_element_clickable(self.PLUS_ICON, timeout=5)
                    self.click(self.PLUS_ICON)
                    logger.info("Clicked plus icon")
                except:
                    logger.info("Trying ADD_BUTTON_GENERIC locator")
                    self.wait_for_element_clickable(self.ADD_BUTTON_GENERIC, timeout=5)
                    self.click(self.ADD_BUTTON_GENERIC)
                    logger.info("Clicked add button")
            self.driver.implicitly_wait(2)
        except Exception as e:
            logger.error(f"Error clicking add icon: {str(e)}")
            raise
    
    def is_product_detail_page_displayed(self):
        
        logger.info("Verifying Product Detail Page is displayed")
        try:
            return self.is_element_displayed(self.PDP_TITLE) and \
                   self.is_element_displayed(self.ADD_TO_CART_BUTTON)
        except:
            return self.is_element_displayed(self.ADD_TO_CART_BUTTON_ALT)
    
    def get_product_title(self):
        
        logger.info("Getting product title")
        return self.get_text(self.PDP_TITLE)
    
    def click_add_to_cart_button(self):
        
        logger.info("Clicking on Add to Cart button")
        try:
            self.click(self.ADD_TO_CART_BUTTON)
        except:
            logger.info("Trying alternate Add to Cart button locator")
            self.click(self.ADD_TO_CART_BUTTON_ALT)
    
    def is_cart_success_message_displayed(self):
        
        logger.info("Checking for cart success message")
        try:
            return self.is_element_displayed(self.CART_SUCCESS_MESSAGE)
        except:
            return False

