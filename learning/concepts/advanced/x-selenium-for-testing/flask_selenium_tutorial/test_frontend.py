import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestFrontendFunctionality:
    def test_page_title(self, chrome_driver, live_server):
        """Test that the page loads with the correct title"""
        chrome_driver.get("http://localhost:5000/")
        assert "Flask Selenium Demo" in chrome_driver.title

    def test_calculator_addition(self, chrome_driver, live_server):
        """Test the calculator addition functionality"""
        chrome_driver.get("http://localhost:5000/")

        # Find input fields and enter values
        num1_input = chrome_driver.find_element(By.ID, "num1")
        num2_input = chrome_driver.find_element(By.ID, "num2")
        
        num1_input.clear()
        num1_input.send_keys("999")
        # time.sleep(5)
        num2_input.clear()
        num2_input.send_keys("1")
        # time.sleep(5)
        # Click the add button
        add_button = chrome_driver.find_element(By.XPATH, "//button[text()='Add']")
        add_button.click()
        import time
        time.sleep(5)
        # Wait for and verify the result
        # result_element = WebDriverWait(chrome_driver, 10).until(
        #     EC.visibility_of_element_located((By.ID, "result"))
        # )
        result_element = chrome_driver.find_element(By.ID, "result")

        assert "Result: 1000" in result_element.text

    def test_calculator_division_by_zero(self, chrome_driver, live_server):
        """Test error handling for division by zero"""
        chrome_driver.get("http://localhost:5000/")

        # Find input fields and enter values
        num1_input = chrome_driver.find_element(By.ID, "num1")
        num2_input = chrome_driver.find_element(By.ID, "num2")

        num1_input.clear()
        num1_input.send_keys("10")

        num2_input.clear()
        num2_input.send_keys("0")

        # Click the divide button
        divide_button = chrome_driver.find_element(
            By.XPATH, "//button[text()='Divide']"
        )
        divide_button.click()

        # Wait for and verify the error message
        result_element = WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )

        assert "Division by zero is not allowed" in result_element.text

    def test_form_submission(self, chrome_driver, live_server):
        """Test the contact form submission"""
        chrome_driver.get("http://localhost:5000/")

        # Fill out the form
        name_input = chrome_driver.find_element(By.ID, "name")
        email_input = chrome_driver.find_element(By.ID, "email")
        message_input = chrome_driver.find_element(By.ID, "message")

        name_input.send_keys("John Doe")
        email_input.send_keys("john@example.com")
        message_input.send_keys("This is a test message")

        # Submit the form
        submit_button = chrome_driver.find_element(
            By.XPATH, "//form[@id='contact-form']//button[@type='submit']"
        )
        submit_button.click()

        # Wait for and verify the result
        result_element = WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.ID, "form-result"))
        )

        assert "Thank you John Doe!" in result_element.text

    def test_dynamic_content_toggle(self, chrome_driver, live_server):
        """Test that the toggle button shows/hides content"""
        chrome_driver.get("http://localhost:5000/")

        # Verify content is initially hidden
        dynamic_content = chrome_driver.find_element(By.ID, "dynamic-content")
        assert "hidden" in dynamic_content.get_attribute("class")

        # Click the toggle button
        toggle_button = chrome_driver.find_element(By.ID, "toggle-button")
        toggle_button.click()

        # Verify content is now visible
        WebDriverWait(chrome_driver, 10).until(EC.visibility_of(dynamic_content))
        assert "hidden" not in dynamic_content.get_attribute("class")

        # Click again to hide
        toggle_button.click()

        # Verify content is hidden again
        WebDriverWait(chrome_driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "dynamic-content"))
        )


if __name__ == "__main__":
    pytest.main()
