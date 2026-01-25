import pyautogui
import time

pyautogui.FAILSAFE = True

# 1. Open Chrome
pyautogui.press("win")
time.sleep(1)
pyautogui.write("chrome", interval=0.1)
pyautogui.press("enter")
time.sleep(5)

# 2. Open PyAutoGUI Quickstart documentation
pyautogui.hotkey("ctrl", "l")
time.sleep(1)
pyautogui.write(
    "https://pyautogui.readthedocs.io/en/latest/quickstart.html",
    interval=0.05
)
pyautogui.press("enter")
time.sleep(10)

# 3. Scroll to load entire page
for _ in range(6):
    pyautogui.press("pagedown")
    time.sleep(1)

# 4. Select all page content
pyautogui.hotkey("ctrl", "a")
time.sleep(1)

# 5. Copy content
pyautogui.hotkey("ctrl", "c")
time.sleep(2)

# 6. Open Notepad
pyautogui.press("win")
time.sleep(1)
pyautogui.write("notepad", interval=0.1)
pyautogui.press("enter")
time.sleep(2)

# 7. Paste content
pyautogui.hotkey("ctrl", "v")
time.sleep(3)

# 8. Save file
pyautogui.hotkey("ctrl", "s")
time.sleep(2)
pyautogui.write("pyautogui_quickstart.txt", interval=0.05)
pyautogui.press("enter")

print("✅ PyAutoGUI documentation copied and saved to Notepad file")
