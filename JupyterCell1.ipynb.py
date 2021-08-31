import urllib.request, urllib.parse, urllib.error
import ssl

ctx = ssl.create_default_context() # ssl - Secure Sockets Layer
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read the HTML from the URL and pass on to BeautifulSoup
url = 'https://www.cia.gov/the-world-factbook/page-data/countries/page-data.json'
print("Opening the file connection...")

uh = urllib.request.urlopen(url, context=ctx)
print("HTTP status",uh.getcode())

html = uh.read().decode()
print(f"Reading done. Total {len(html)} characters read. \n")

print(html)
