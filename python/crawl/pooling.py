import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://www.hsph.harvard.edu/pooling-project/cohort-study-participants/', headers=headers)
# get div with class 'entry-content'
soup = BeautifulSoup(r.text, 'html.parser')
div = soup.find_all('div', {'class': 'entry-content'})[0]
# get all p tags
ps = div.find_all('p')
data = []
for p in ps:
    # get strong tag
    strong = p.find('strong')
    # check if a tag is present in strong tag
    if p.find('a') is not None:
        a = p.find('a')
        name = a.text
        acronym = strong.text.strip().replace('(', '').replace(')', '')
    else:
        name = strong.text
        # match parenthesis
        match = re.search('\((.+)\)', name)
        acronym = match.group(1)
        # remove parenthesis from name
        name = name.replace(f' ({acronym})', '')
    # find br tag in p
    br = p.find('br')
    description = br.text
    data.append([name, acronym, description])
df = pd.DataFrame(data, columns=['name', 'acronym', 'description'])
df.to_csv('../data/pooling.csv', index=False)