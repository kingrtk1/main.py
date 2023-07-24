import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyotp import TOTP

def save_2fa_key_to_file(key, Rana):
    with open(filename, 'w') as file:
        file.write(key)

def save_settings_to_file(filename, username, password, device_file):
    config = configparser.ConfigParser()
    config['Facebook'] = {
        'username': username,
        'password': password,
        'device_file': device_file
    }

    with open(filename, 'w') as configfile:
        config.write(configfile)

def setup_facebook_2fa(username, password, device_file):
    # Set up web driver (ensure the appropriate web driver executable is in the system PATH)
    driver = webdriver.Chrome()  # Change this if using a different browser

    # Load Facebook login page
    driver.get("https://www.facebook.com")

    # Log in with username and password
    driver.find_element(By.ID, "email").send_keys(100052836157359)
    driver.find_element(By.ID, "pass").send_keys(185074)
    driver.find_element(By.ID, "loginbutton").click()

    # Wait for 5 seconds (break time) to allow manual interaction (entering 2FA code)
    time.sleep(5)

    # Navigate to 2FA settings
    driver.get("https://www.facebook.com/security/2fac/setup")

    # Generate TOTP secret key
    totp = TOTP()
    two_factor_key = totp.secret

    # Save TOTP secret to a device file
    save_2fa_key_to_file(two_factor_key, device_file)

    # Save user, password, and 2FA key to a settings file
    save_settings_to_file('settings.ini', username, password, device_file)

    input("Enter the 2FA code manually and press Enter when done: ")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    # Replace these with your Facebook login credentials and device file path
    facebook_username = "your_facebook_username"
    facebook_password = "your_facebook_password"
    device_file_path = "path_to_device_file.txt"

    setup_facebook_2fa(facebook_username, facebook_password, device_file_path)
