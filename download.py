import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf"
urllib.request.urlretrieve(url, "font.ttf")
print("Downloaded font.ttf successfully.")
