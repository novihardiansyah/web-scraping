import urllib.request, urllib.parse, urllib.error
import ssl
import json

ctx = ssl.create_default_context() # ssl - Secure Sockets Layer
ctx.check_hostname = False # No get hostname
ctx.verify_mode = ssl.CERT_NONE # ssl get no certificate

# Read the HTML from the URL and pass
url = 'https://www.cia.gov/the-world-factbook/page-data/countries/page-data.json'
print("Opening the file connection...")

uh = urllib.request.urlopen(url, context=ctx) # <http.client.HTTPResponse at 0x2200d6b4888>
print("HTTP status", uh.getcode()) # Get Status URL

html = uh.read().decode() # Read and Decode
print(f"Reading done. Total {len(html)} characters read. \n") # Get Length of html

getjson = json.loads(html)

smaljson = getjson['result']['data']['countries']['edges']
smaljson2 = len(smaljson)
print(f"Array {smaljson2}.\n")

theurl = 'https://www.cia.gov'

def geteenumer(xxx):
    for idx, val in enumerate(xxx):
        getjson3 = val['node']['path']
        mixgeturl = theurl + getjson3
        print(mixgeturl)
        
takeenumer = geteenumer(smaljson)
