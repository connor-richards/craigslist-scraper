#!/usr/bin/python3.5

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

site = 'https://chico.craigslist.org/d/sporting-goods/search/sga?s='
html = urlopen(site)
file = open("pid.txt", "a")
soup = BeautifulSoup(html, "html5lib")

#find total count of results
total = soup.find("span", class_="totalcount")
total = ''.join(filter(lambda i: i.isdigit(), total))
total = int(total)

#verify command line args
if len(sys.argv) != 4:
  print("Error: usage \"craigScrape.py <query> <maxprice> <numproducts>\"")
  exit(1)
query = str(sys.argv[1]).lower()
maxp = int(sys.argv[2])
nump = int(sys.argv[3])

#gather all data
prices = []
names = []
idx = 0
while idx < total:
  site = 'https://chico.craigslist.org/d/sporting-goods/search/sga?s='+str(idx)
  html = urlopen(site)
  file = open("pid.txt", "a")
  soup = BeautifulSoup(html, "html5lib")

  #find prices
  for listing in soup.find_all("span", class_="result-meta"):
    priceidx = listing.find("span", class_="result-price")
    if priceidx != None:
      price = priceidx.text[:].strip().replace("$", "").replace(",","")
      price = int(float(price))
      prices.append(price)

  #find names
  for listing in soup.find_all("a", class_="result-title hdrlnk"):
    name = str(listing.text[:])
    names.append(name)

  idx = idx+120

#compile results
results = []
idx = 0
while idx < len(names):
  namestr = names[idx].lower()
  if namestr.find(query) >= 0:
    if prices[idx] <= maxp:
      sublist = [names[idx], prices[idx], 'Chico']
      #insert in ascending order by price
      if len(results) == 0:
        results.append(sublist)
      else:
        idx2 = 0
        while idx2 < len(results):
          if int(prices[idx]) < int(results[idx2][1]):
            sublist[1] = str(sublist[1])
            results.insert(idx2, sublist)
            break
          idx2 = idx2+1
  idx = idx+1

#user only wants numProducts
shortresults = []
idx = 0
for entry in results:
  if idx > nump-1:
    break;
  shortresults.append(entry)
  idx = idx+1

#instantiate file, if not there
csvfile = '/scrapeData.csv'
csvfile = os.getcwd() + csvfile
os.system('touch ' + csvfile)

#check if top 5 changed, for email
email = 0
olddata = []
with open(csvfile, newline='') as fd:
  reader = csv.reader(fd)
  olddata = list(reader)
#compare first 5 if list sizes match
if len(olddata)-1 == len(shortresults):
  if len(shortresults) > 0:
    idx = 0
    while idx < len(shortresults) and idx < 5:
      #set email flag if there is a difference
      if olddata[idx+1] != shortresults[idx]:
        email = 1
        break
      idx = idx+1
#set email flag if list sizes don't match
else:
  email = 1

#create csv
fields = ['Title', 'Price', 'City']
with open(csvfile, 'w') as fd:
  write = csv.writer(fd)
  write.writerow(fields)
  write.writerows(shortresults)

#create and send email if necessary
if email == 1:
  msg = MIMEMultipart()
  msg['From'] = 'connor.richards899@gmail.com'
  msg['To'] = 'makingthings3@gmail.com'
  msg['Subject'] = 'Python: Your Craiglist listings updated'

  message = 'There was a change in the top 5 listings of your search.\nThe new file has been attached.'
  msg.attach(MIMEText(message))

  part = MIMEBase('application', "octet-stream")
  part.set_payload(open(csvfile, "rb").read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', 'attachment; filename="scrapeData.csv"')
  msg.attach(part)

  mailserver = smtplib.SMTP('smtp.gmail.com', 587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login('connor.richards899@gmail.com', 'wtkmarpefpzslsex')
  mailserver.sendmail('connor.richards899@gmail.com', 'makingthings3@gmail.com', msg.as_string())
  mailserver.quit()

  print("Change Detected: Email Sent")
else:
  print("NO Change Detected")
