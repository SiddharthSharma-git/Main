
from appium.webdriver.common.appiumby import AppiumBy
from base.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@text="Email"]')
    PASSWORD_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@text="Password"]')
    SIGN_IN_BUTTON = (AppiumBy.XPATH, '(//android.widget.TextView[@text="Sign In"])[4]')
    FORGOT_PASSWORD_LINK = (AppiumBy.XPATH, "//android.widget.TextView[@text='Forgot Password']")
    CREATE_ACCOUNT_BUTTON = (AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='auth-secondary-action']")
    ERROR_MESSAGE = (AppiumBy.ID, "com.mumzworld.android:id/error_message")
    
    def __init__(self, driver):
       
        super().__init__(driver)
        self.logger.info("Login Page initialized")
    
    def enter_email(self, email: str):
        
        self.logger.info(f"Entering email: {email}")
        self.wait_for_element_clickable(self.EMAIL_FIELD, timeout=10)
        self.send_keys(self.EMAIL_FIELD, email)
    
    def enter_password(self, password: str):
        
        self.logger.info("Entering password")
        self.send_keys(self.PASSWORD_FIELD, password)
    
    def click_sign_in_button(self):
        
        self.logger.info("Clicking sign in button")
        self.click(self.SIGN_IN_BUTTON)
    
    def login(self, email: str, password: str):
        
        self.logger.info(f"Logging in with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.hide_keyboard()
        self.click_sign_in_button()
    
    def is_error_message_displayed(self) -> bool:
        
        return self.is_element_displayed(self.ERROR_MESSAGE)
    
    def get_error_message(self) -> str:
        
        return self.get_text(self.ERROR_MESSAGE)
    
    def click_forgot_password(self):
        
        self.logger.info("Clicking forgot password link")
        self.click(self.FORGOT_PASSWORD_LINK)

