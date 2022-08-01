import subprocess
from selenium import webdriver
chrom_path = r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrom_path)
link = 'https://reddit.com'
driver.get(link)

s = driver.page_source
print((s.encode("utf-8")))
subprocess.call("TASKKILL /f  /IM  CHROME.EXE")