import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('https://www.ukri.org/councils/mrc/facilities-and-resources/find-an-mrc-facility-or-resource/cohort-directory/')
soup = BeautifulSoup(r.text, 'html.parser')
# get all h2 tags
h2s = soup.find_all('h2')[:-4]
data = []
for h2 in h2s:
    name = h2.text
    # get paragraph text just after h2 tag
    p = h2.find_next('p').text
    # get all li children tags
    lis = h2.find_next('ul').find_all('li')
    row = [name, p]
    cols = []
    for li in lis:
        regex = re.search('(.+):\s(.+)', li.text)
        cols.append(regex.group(1))
        row.append(regex.group(2))
    if len(cols) > 8:
        data.append(row)
        C = cols
    else:
        row.append('')
        
df = pd.DataFrame(data, columns=['name', 'description'] + C)
df.to_csv('../data/ukri_cohorts.csv', index=False)    