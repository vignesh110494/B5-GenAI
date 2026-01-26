from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/")
# driver.back()
# driver.forward()
# driver.refresh()    

#finding element

# element = driver.find_element(By.ID, "content")
element = driver.find_element(By.XPATH, '//*[@id="content"]/ul/li[1]/a') 
print(element)

#wait
wait = WebDriverWait(driver,100)
element = wait.until(EC.presence_of_element_located((By.ID, "content")))

#interact with element
element.click()
element.send_keys('test')
element.clear()


#driverscreenshot
driver.save_screenshot("screenshot.png")



