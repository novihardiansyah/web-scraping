import pandas as pd
import numpy as np
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
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

country_names=[]
country_url=[]

for idx, val in enumerate(smaljson):
    getjson2 = val['node']['title']
    
    getjson3 = val['node']['path']
    mixgeturl = theurl + getjson3
    
    country_names.append(getjson2)
    country_url.append(mixgeturl)

demographics1=[]
demographics2=[]
demographics3=[]
demographics4=[]
demographics5=[]

offset = len('65 years and over:\n')

# Iterate over every country
for idx, val in enumerate(smaljson):
    getjson2 = val['node']['title']
    
    getjson3 = val['node']['path']
    mixgeturl = theurl + getjson3
    
    html = urllib.request.urlopen(mixgeturl, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    txt=soup.get_text()
    pos1=txt.find('0-14 years: ')
    pos2=txt.find('15-24 years: ')
    pos3=txt.find('25-54 years: ')
    pos4=txt.find('55-64 years: ')
    pos5=txt.find('65 years and over: ')
    
    if pos1==-1:
        print(f"**0-14 years % data not found for {country_names[idx]}!**")
        demographics1.append(np.nan)
    else:
        text=txt[pos1+12:pos1+18]
        end = re.search('%',text).start() # PROSES HILANGKAN PERSEN (%)
        a = float((txt[pos1+12:pos1+12+end]))
        demographics1.append(a)
        print(f"0-14 years % data extraction complete for {country_names[idx]}!")
    
    if pos2==-1:
        print(f"**15-24 years % data not found for {country_names[idx]}!**")
        demographics2.append(np.nan)
    else:
        text = txt[pos2+13:pos2+19]
        end = re.search('%',text).start()
        a = float((txt[pos2+13:pos2+13+end]))
        demographics2.append(a)
        print(f"15-24 years % data extraction complete for {country_names[idx]}!")
        
    if pos3==-1:
        print(f"**25-54 years % data not found for {country_names[idx]}!**")
        demographics3.append(np.nan)
    else:
        text = txt[pos3+13:pos3+19]
        end = re.search('%',text).start()
        a = float((txt[pos3+13:pos3+13+end]))
        demographics3.append(a)
        print(f"25-54 years % data extraction complete for {country_names[idx]}!")
    
    if pos4==-1:
        print(f"**55-64 years % data not found for {country_names[idx]}!**")
        demographics4.append(np.nan)
    else:
        text = txt[pos4+13:pos4+19]
        end = re.search('%',text).start()
        a = float((txt[pos4+13:pos4+13+end]))
        demographics4.append(a)
        print(f"55-64 years % data extraction complete for {country_names[idx]}!")
    
    
    if pos5==-1:
        print(f"**65 years and beyond % data not found for {country_names[idx]}!**")
        demographics5.append(np.nan)
    else:
        text = txt[pos5+offset:pos5+offset+6]
        end = re.search('%',text).start()
        a = float((txt[pos5+offset:pos5+offset+end]))
        demographics5.append(a)
        print(f"65 years and beyond % data extraction complete for {country_names[idx]}!")

# SAVE TO CSV
data={
    '0-14 years old %':demographics1,
    '15-24 years %':demographics2,
    '25-54 years %':demographics3,
    '55-64 years %':demographics4,
    '65 years and above %':demographics5
}
#df1=pd.DataFrame(data=data,index=country_names[1:5])

df_demo=pd.DataFrame(data=data,index=country_names[0:len(country_url)])
df_demo.index.name='COUNTRY'
df_demo.dropna(inplace=True)
df_demo

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('AgeStructure.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df_demo.to_excel(writer, sheet_name='Demographics 2020 est.')
# Close the Pandas Excel writer and output the Excel file.
writer.save()
