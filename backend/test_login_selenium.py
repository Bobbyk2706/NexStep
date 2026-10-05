from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
TEST_EMAIL = "vivek.pytest@nexstep.example"
TEST_PASSWORD = "Vivek@123"


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def test_valid_student_login():
    driver = create_driver()

    try:
        driver.get(f"{BASE_URL}/login")

        wait = WebDriverWait(driver, 10)

        email = wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        password = driver.find_element(By.ID, "password")

        email.send_keys(TEST_EMAIL)
        password.send_keys(TEST_PASSWORD)
        password.send_keys(Keys.ENTER)

        # Wait for the login request/navigation to complete.
        wait.until(
            EC.url_changes(f"{BASE_URL}/login")
        )

        assert "/login" not in driver.current_url

    finally:
        input("Press Enter to close browser...")
        driver.quit()


def test_invalid_student_login():
    driver = create_driver()

    try:
        driver.get(f"{BASE_URL}/login")

        wait = WebDriverWait(driver, 10)

        email = wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        password = driver.find_element(By.ID, "password")

        email.send_keys(TEST_EMAIL)
        password.send_keys("WrongPassword123")
        password.send_keys(Keys.ENTER)

        # The user should remain on the login page after invalid credentials.
        wait.until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        assert "/login" in driver.current_url

    finally:
        driver.quit()