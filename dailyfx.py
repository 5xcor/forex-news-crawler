import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

#Get data
data = requests.get('https://www.dailyfx.com/calendar')

#Get html content
html = data.content

#Parse html with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

#Get all tables
tables = soup.find_all('table', class_ = 'table dfx-calendar-table tab-pane fade')

#List from each extract
pure = []
#Store extracted data
extract = {}

#Read table in tables
for table in tables:
    #Get date in  class'eco-table-date' element
    date = table.find('div', class_ = 'eco-table-date').text.strip()
    #Convert date format
    date = datetime.datetime.strptime(date, '%A, %B %d, %Y').strftime('%d-%m-%Y')
    extract['date'] = date
    
    #Get all rows
    rows = table.find_all('tr', class_ = 'jsdfx-searched-item')

    #Read row in table skip first row
    for row in rows:
        #Get all cols
        col = row.find_all('td')

        #Get time
        extract['time'] = col[0].text.strip()
        #Get country
        extract['country'] = col[2].find('div')['data-filter']
        #Get event and remove first 5 character
        extract['event'] = col[3].text.strip()[5:]
        #Get impact
        extract['impact'] = col[4].find('span').text.strip()
        #Get actual
        extract['actual'] = col[5].text.strip()
        #Get forecast
        extract['forecast'] = col[6].text.strip()
        #Get previous
        extract['previous'] = col[7].text.strip()

        pure.append(dict(extract))

#Make pandas DateFrame
data = pd.DataFrame(pure)
#Save to csv file
data.to_csv('dailyfx.csv', index=False)