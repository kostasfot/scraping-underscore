# Importing modules and packages
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# Scrape single game shots
base_url = 'https://understat.com/match/'
match = str(input('Please enter the match ID:'))
url = base_url + match

res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')
scripts = soup.find_all('script')

# Get only the shots data
strings = scripts[1].string

# Strip symbols so we only have the json data
ind_start = strings.index("('") + 2
ind_end = strings.index("')")

json_data = strings[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

# Convert to json format
data = json.loads(json_data)

x = list()
y = list()
xg = list()
team = list()
data_away = data['a']
data_home = data['h']

for index in range(len(data_home)) :
    for key in data_home[index] :
        if key == 'X' :
            x.append(data_home[index][key])
        if key == 'Y' :
            y.append(data_home[index][key])
        if key == 'xG' :
            xg.append(data_home[index][key])
        if key == 'h_team' :
            team.append(data_home[index][key])
            
for index in range(len(data_away)) :
    for key in data_away[index] :
        if key == 'X' :
            x.append(data_away[index][key])
        if key == 'Y' :
            y.append(data_away[index][key])
        if key == 'xG' :
            xg.append(data_away[index][key])
        if key == 'a_team' :
            team.append(data_away[index][key])
            
# Create the data frame
col_names = ['x', 'y', 'xg','team']
df = pd.DataFrame([x, y, xg, team], index=col_names)
df = df.T

df.to_csv(f'{match}.csv')