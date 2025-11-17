import pytest
import allure
from pageObjects.account_page import AccountPage
from pageObjects.login_page import LoginPage
from pageObjects.product_page import ProductPage
from pageObjects.cart_page import CartPage
from util.logger import Logger


logger = Logger.get_logger(__name__)


@allure.feature('Mumzworld App')
class TestMumzworld:

    
    @allure.title("Test successful login")
    @allure.story('Login')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login(self, driver):

        logger.info("=" * 80)
        logger.info("Starting test: test_successful_login")
        logger.info("=" * 80)

        account_page = AccountPage(driver)
        login_page = LoginPage(driver)

        username = "ersharma.siddharth@gmail.com"
        password = "GoOgle@96"

        with allure.step("App is opened"):
            logger.info("App is already opened")
            driver.implicitly_wait(3)

        with allure.step("Navigate to Account tab"):
            try:
                account_page.click_account_tab()
                logger.info("Clicked on Account tab")
            except:
                logger.info("Already on Account tab")
            driver.implicitly_wait(2)

        with allure.step("Click on Sign In button"):
            account_page.click_sign_in_button()
            logger.info("Clicked on Sign In button")
            driver.implicitly_wait(2)

        with allure.step(f"Enter email: {username}"):
            login_page.enter_email(username)
            logger.info(f"Entered email: {username}")
        
        with allure.step("Enter password"):
            login_page.enter_password(password)
            logger.info("Entered password")
        
        with allure.step("Click Sign In button"):
            login_page.click_sign_in_button()
            logger.info("Clicked Sign In button")

        with allure.step("Verify user account information is displayed"):

            driver.implicitly_wait(10)

            account_page.click_account_tab()
            driver.implicitly_wait(3)

            is_logged_in = account_page.is_account_info_displayed() or \
                          account_page.is_logged_in()
            
            assert is_logged_in, "Login failed - Account information not displayed"
            logger.info("Login successful - Account information displayed")
        
        logger.info("=" * 80)
        logger.info("Test completed: test_successful_login - PASSED")
        logger.info("=" * 80)

    def test_invalid_login(self, driver):

        logger.info("=" * 80)
        logger.info("Starting test: test_invalid_login")
        logger.info("=" * 80)

        account_page = AccountPage(driver)
        login_page = LoginPage(driver)

        username = "wrong@example.com"
        password = "wrongpassword"

        with allure.step("App is opened"):
            driver.implicitly_wait(3)

        with allure.step("Navigate to Account tab"):
            try:
                account_page.click_account_tab()
                logger.info("Clicked on Account tab")
            except:
                logger.info("Already on Account tab")
            driver.implicitly_wait(2)

        with allure.step("Click on Sign In button"):
            account_page.click_sign_in_button()
            driver.implicitly_wait(2)

        with allure.step(f"Enter invalid email: {username}"):
            login_page.enter_email(username)

        with allure.step("Enter invalid password"):
            login_page.enter_password(password)

        with allure.step("Click Sign In button"):
            login_page.click_sign_in_button()
            driver.implicitly_wait(5)

        with allure.step("Verify error message is displayed"):
            error_message = login_page.get_error_message()
            logger.info(f"Error message displayed: {error_message}")
            assert (
                    "invalid" in error_message.lower()
                    or "incorrect" in error_message.lower()
                    or "error" in error_message.lower()
            ), "Expected error message not displayed"

        logger.info("=" * 80)
        logger.info("Test completed: test_invalid_login - PASSED")
        logger.info("=" * 80)

    @allure.title("Test successful add to cart")
    @allure.story('Shopping Cart')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_successful_add_to_cart(self, driver):

        logger.info("=" * 80)
        logger.info("Starting test: test_successful_add_to_cart")
        logger.info("=" * 80)

        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        search_item = "Diaper"
        with allure.step("App is opened"):
            logger.info("App is already opened")

        with allure.step(f"Search for item: {search_item}"):
            product_page.enter_search_text(search_item)
            logger.info(f"Searched for: {search_item}")
            driver.implicitly_wait(2)

        with allure.step("Select first search suggestion from dropdown"):
            product_page.select_first_search_suggestion()
            logger.info("Selected first search suggestion")
            driver.implicitly_wait(3)

        with allure.step("Click on + icon to add item to cart"):
            product_page.click_add_icon()
            logger.info("Clicked on + icon to add to cart")
            driver.implicitly_wait(3)

        with allure.step("Navigate to Cart"):
            cart_page.click_cart_tab()
            logger.info("Navigated to Cart")
            driver.implicitly_wait(3)
        
        with allure.step("Verify item is present in cart"):
            assert cart_page.is_item_in_cart(), \
                "Item not found in cart after adding"
            logger.info("Item successfully added to cart")

            try:
                item_count = cart_page.get_cart_items_count()
                logger.info(f"Cart items count: {item_count}")
            except:
                logger.info("Could not retrieve cart item count")
        
        logger.info("=" * 80)
        logger.info("Test completed: test_successful_add_to_cart - PASSED")
        logger.info("=" * 80)

