from seleniumwire import webdriver
from selenium_stealth import stealth
import time


options = webdriver.ChromeOptions()
options.add_argument("--max-gum-fps")
options.add_argument("--enable-usermedia-screen-capturing")
options.add_argument("--enable-audio-debug-recordings-from-extension")
options.add_argument("--agc-startup-min-volume")
options.add_argument("--alsa-input-device")
options.add_argument("--alsa-input-device")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Ubuntu; "
    "Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    executable_path="webdriver/chromedriver",
    options=options,
)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)


url = "https://bot.sannysoft.com/"

driver.get(url)
time.sleep(10)
driver.quit()