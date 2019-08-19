import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

#Get data
data = requests.get('https://www.babypips.com/economic-calendar')

#Get html content
html = data.content

#Parse html with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

#Get all tables
tables = soup.find_all('div', class_ = 'calendar-section calendar-table-day')

#List from each extract
pure = []
#Store extracted data
extract = {}

#Read table in tables
for table in tables:
    #Get date in  class'eco-table-date' element
    day = table.find('div', class_ = 'day').text.strip()
    month = table.find('div', class_ = 'month').text.strip()
    year = datetime.datetime.now().year
    #Convert date format
    month = datetime.datetime.strptime(month, '%b').strftime('%m')
    date = '{}-{}-{}'.format(day, month, year)
    extract['date'] = date
    
    #Get all rows
    rows = table.find_all('tr', class_ = 'calendar-table-event-row')

    #Read row in table skip first row
    for row in rows:
        #Get all cols
        col = row.find_all('td')

        #Get time
        extract['time'] = col[0].text.strip()
        #Get country
        extract['country'] = col[1].find('div', class_ = 'currency-code').text.strip()
        #Get event and remove first 5 character
        extract['event'] = col[2].find('a').text.strip()
        #Get impact
        extract['impact'] = col[3].find('div').text.strip()
        #Get actual
        extract['actual'] = col[4].text.strip()
        #Get forecast
        extract['forecast'] = col[5].text.strip()
        #Get previous
        extract['previous'] = col[6].text.strip()

        pure.append(dict(extract))

#Make pandas DateFrame
data = pd.DataFrame(pure)
#Save to csv file
data.to_csv('babypips.csv', index=False)
