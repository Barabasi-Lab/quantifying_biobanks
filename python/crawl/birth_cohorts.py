# Birthcohorts.net crawler
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = requests.get('https://www.birthcohorts.net/birthcohorts/list/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# get ul tag with id 'bc_list'
ul = soup.find_all('ul', {'id': 'bc_list'})[0]
# get all li tags
lis = ul.find_all('li')
links = []
data = []
for li in lis:
    text = li.text
    match = re.search('(.+)Enrollment: (.+)Expected number of children in cohort: '
                      '(\d+)(.+)', text)
    name = match.group(1)
    enrolment = match.group(2)
    size = match.group(3)
    pi_institution = match.group(4)
    pi_institution = pi_institution[:-12]
    data.append([name, enrolment, size, pi_institution])
    # get first a tag
    a = li.find_all('a')[0]
    links.append([name, a['href']])
    
df = pd.DataFrame(data, columns=['name', 'enrolment', 'size', 'PI_and_institution'])
df_links = pd.DataFrame(links, columns=['name', 'link'])
df.to_csv('../data/birthcohorts.csv', index=False)
df_links.to_csv('../data/birthcohorts_links.csv', index=False)
        