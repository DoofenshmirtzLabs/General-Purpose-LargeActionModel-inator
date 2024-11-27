from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, render_template, send_file
import time
import os

app = Flask(__name__)

def take_screenshot(driver, step_name):
    """
    Takes a screenshot of the current browser state.
    """
    screenshot_path = f"screenshots/{step_name}.png"
    os.makedirs("screenshots_v2", exist_ok=True)
    driver.save_screenshot(screenshot_path) 
    print("screen shot taken\n")
    return screenshot_path

@app.route("/")
def show_screenshot():
    """
    Displays the latest screenshot on a web page.
    """
    latest_screenshot = sorted(os.listdir("screenshots"))[-1]
    return render_template("index.html", image_path=f"screenshots/{latest_screenshot}")

def automate_with_visuals(driver):
    """
    Automates a task and saves screenshots after each step.
    """
    # Step 1: Open Netflix login page
    driver.get("https://www.netflix.com/login")
    take_screenshot(driver, "step1_open_page")
    time.sleep(2)

    # Step 2: Fill in email
    email_input = driver.find_element(By.NAME, "userLoginId")
    email_input.send_keys("user@example.com")
    take_screenshot(driver, "step2_fill_email")

    # Step 3: Fill in password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("password123")
    take_screenshot(driver, "step3_fill_password")

    # Step 4: Click the sign-in button
    sign_in_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
    sign_in_button.click()
    take_screenshot(driver, "step4_click_signin")
    time.sleep(5)

if __name__ == "__main__":
    # Launch browser
    driver = webdriver.Chrome()

    try:
        # Automate the task with visuals
        automate_with_visuals(driver)

        # Start the Flask server
        app.run(debug=True)
    finally:
        # Close the browser
        driver.quit()
