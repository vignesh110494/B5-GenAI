from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# ---------- SETUP ----------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# ---------- 1. PAGE LOAD ----------
driver.get("https://the-internet.herokuapp.com/")
wait.until(EC.title_contains("The Internet"))
print("✅ Page loaded")

wait = WebDriverWait(driver, 100)
# ---------- 2. A/B TESTING ----------
ab_testing = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "A/B Testing")))
ab_testing.click()
wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
print("✅ A/B Testing opened")
driver.back()
wait = WebDriverWait(driver, 100)
# ---------- 3. CHECKBOXES ----------
checkbox_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkboxes")))
checkbox_link.click()

checkboxes = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']"))
)

if not checkboxes[0].is_selected():
    checkboxes[0].click()
if checkboxes[1].is_selected():
    checkboxes[1].click()

print("✅ Checkboxes tested")
driver.back()
wait = WebDriverWait(driver, 100)
# ---------- 4. DROPDOWN ----------
dropdown_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Dropdown")))
dropdown_link.click()

dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "dropdown"))))
dropdown.select_by_visible_text("Option 2")

print("✅ Dropdown tested")
driver.back()
wait = WebDriverWait(driver, 100)
# ---------- 5. JAVASCRIPT ALERT ----------
alerts_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "JavaScript Alerts")))
alerts_link.click()

alert_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']"))
)
alert_btn.click()

wait.until(EC.alert_is_present())
alert = driver.switch_to.alert
alert.accept()

print("✅ JavaScript alert handled")
driver.back()
wait = WebDriverWait(driver, 100)
# ---------- 6. FILE UPLOAD ----------
upload_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "File Upload")))
upload_link.click()

# Create a temporary file to upload
file_path = os.path.abspath("selenium-vignesh-upload.txt")
with open(file_path, "w") as f:
    f.write("Selenium File Upload Test")

upload_input = wait.until(EC.presence_of_element_located((By.ID, "file-upload")))
upload_input.send_keys(file_path)

submit_btn = driver.find_element(By.ID, "file-submit")
submit_btn.click()

uploaded_text = wait.until(
    EC.presence_of_element_located((By.ID, "uploaded-files"))
)
assert "selenium-vignesh-upload.txt" in uploaded_text.text

print("✅ File upload tested")
driver.back()
wait = WebDriverWait(driver, 100)
