from bs4 import BeautifulSoup
import undetected_chromedriver as webdriver
import requests
from selenium.webdriver.chrome.service import Service
import os
from webdriver_manager.chrome import ChromeDriverManager
import time

# url = "https://character.ai"
# download_folder = "character_ai_downloads"
# os.makedirs(download_folder, exist_ok=True)

# # Set up the selenium web driver
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

# # options.headless = True

# service = Service(ChromeDriverManager().install())

# # driver_path = "/path/to/chromedriver"  # UPDATE THIS PATH
# driver = webdriver.Chrome(version_main=116, options=options)

import undetected_chromedriver as uc

# path_to_chromedriver = 'chrome-mac-arm64/testing.app'  # Make sure to replace this with your actual path
service = Service(ChromeDriverManager(driver_version="114.0.5735.90").install())
driver = uc.Chrome(service=service, headless=False)
driver.get('https://character.ai')
driver.save_screenshot('nowsecure.png')

# Start by navigating to the domain
driver.get("https://beta.character.ai/")

# Adding cookies
cookies = [
    {"name": "_ga", "value": "GA1.2.107291823.1691696773"},
    {"name": "sessionid", "value": "48z6obgolfw433o7u0hhm2isbsn5v6xs"},
    # Add other cookies similarly...
]

for cookie in cookies:
    driver.add_cookie(cookie)

# Now you can navigate or refresh to use the cookies you've set:
driver.get("https://beta.character.ai/")

# driver.implicitly_wait(60)  # waits for 10 seconds
time.sleep(1000)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Download function for resources
def download_resource(link, attr):
    try:
        resource_url = link[attr]
        if not (resource_url.startswith("http") and resource_url.startswith("//")):
            if resource_url.startswith("/"):
                resource_url = url + resource_url
            else:
                resource_url = url + "/" + resource_url

        filename = os.path.join(download_folder, os.path.basename(resource_url))
        with open(filename, 'wb') as file:
            file.write(requests.get(resource_url).content)
        link[attr] = os.path.basename(resource_url)
    except Exception as e:
        print(f"Failed to download {resource_url}. Error: {e}")

# Find and download each resource
for link in soup.find_all(['script', 'img', 'link']):
    if link.name == "script" and link.has_attr("src"):
        download_resource(link, "src")
    elif link.name == "img" and link.has_attr("src"):
        download_resource(link, "src")
    elif link.name == "link" and link.has_attr("href"):
        download_resource(link, "href")

# Save the updated HTML
with open(os.path.join(download_folder, "index.html"), "w", encoding="utf-8") as f:
    f.write(str(soup))

driver.quit()
print("Resources downloaded and saved!")
