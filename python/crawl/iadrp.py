# International Alzheimer’s and Related Dementias Research Portfolio
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = requests.get('https://iadrp.nia.nih.gov/about/cadro/Population-Studies-Cohorts-and-Studies', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
# get first div tag with class 'grid-col-fill'
div = soup.find_all('div', {'class': 'grid-col-fill'})[0]
# get first ul tag after div
ul = div.find_all('ul')[0]
# get all li tags
lis = ul.find_all('li')
data = []
for li in lis:
    # get text
    text = li.text
    # use regex to get only the last parenthesis and the text before it
    match = re.search('(.+)\s\((.+)\)$', text)
    name = match.group(1)
    parms = match.group(2)
    data.append([name, parms])
df = pd.DataFrame(data, columns=['name', 'parameters'])
df.to_csv('../data/iadrp_cohorts.csv', index=False)