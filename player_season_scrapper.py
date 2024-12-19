import pandas as pd 
import requests
from bs4 import BeautifulSoup
import datetime
import random

today = datetime.date.today()
current_year = today.year + 1
years = list(range(1876,current_year))

# Create the lists that will be turned into a dataframe
season = []
first_name = []
last_name = []
link = []
position = []
team = []
games_played = []
at_bats = []
runs = []
hits = []
doubles = []
triples = []
homeruns = []
rbi = []
walks = []
strikeouts = []
stolen_bases = []
caught_stealing = []
batting_average = []
on_base_percentage = []
slugging_percentage = []
on_base_plus_slugging = []

chrome_user_agent_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
                            ]

for year in years:
    print('Creating url for season '+ str(year)+ ' # of pages')
    url = 'https://www.mlb.com/stats/'+ str(year) +'/regular-season?page=1&playerPool=ALL'
    custom_headers = {'user-agent': random.choice(chrome_user_agent_list)}
    r = requests.get(url, headers= custom_headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    page_html = soup.find('div', class_ = 'bui-button-group pagination bui-button-group')
    page_links = page_html.findAll('button')
    pages = []
    for button in page_links:
        item = int(button['value'])
        pages.append(item)
    max_page = int(max(pages)) + 1
    page_count = list(range(1,max_page))
    print('page count for ' + str(year))
    print(page_count)

    for page in page_count:
        print('grabbing stats for season ' + str(year) + '; Page: ' + str(page))
        url = 'https://www.mlb.com/stats/'+ str(year) +'/regular-season?page='+ str(page) +'&playerPool=ALL' 
        
        custom_headers = {'user-agent': random.choice(chrome_user_agent_list)}
        
        r = requests.get(url, headers= custom_headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        results = soup.find('div', class_ = 'stats-body-table player')

        player_name = results.findAll('span', class_="full-G_bAyq40")
        player_link = results.findAll('a', class_="bui-link")
        player_position = results.findAll('div', class_="position-SAxuJGcx")
        season_team = results.findAll('td', class_="col-group-end-BOW7diD7 number-GoaicxKV align-left-L6MdxTlJ is-table-pinned-lGP8KWTK")
        stats = results.findAll('td')


        # Create Player First and Last Name Columns
        f_count = 0
        l_count = 0
        for name in player_name:
            if f_count > l_count:
                last_name.append(name.text)
                l_count = l_count + 1
                continue
            if f_count == l_count:
                first_name.append(name.text)
                f_count = f_count + 1
                continue
        
        # Create Season column
        for i in range(f_count):
            current_season = year
            season.append(current_season)
        
        # Create Player Position Column
        for i in player_position:
            pos = i.text
            position.append(pos)
        
        #Create the link column
        for a in player_link:
            item = a['href']
            if 'player' in item:
                link.append(item)

        # Create the list for number of games played in the season
        counter = 0
        for stat in stats:
            i = stat.text
            if counter == 0:
                team.append(i)
                counter = counter + 1
                continue
            if counter == 1:
                games_played.append(i)
                counter = counter + 1
                continue
            if counter == 2:
                at_bats.append(i)
                counter = counter + 1
                continue
            if counter == 3:
                runs.append(i)
                counter = counter + 1
                continue
            if counter == 4:
                hits.append(i)
                counter = counter + 1
                continue
            if counter == 5:
                doubles.append(i)
                counter = counter + 1
                continue
            if counter == 6:
                triples.append(i)
                counter = counter + 1
                continue
            if counter == 7:
                homeruns.append(i)
                counter = counter + 1
                continue
            if counter == 8:
                rbi.append(i)
                counter = counter + 1
                continue
            if counter == 9:
                walks.append(i)
                counter = counter + 1
                continue
            if counter == 10:
                strikeouts.append(i)
                counter = counter + 1
                continue
            if counter == 11:
                stolen_bases.append(i)
                counter = counter + 1
                continue
            if counter == 12:
                caught_stealing.append(i)
                counter = counter + 1
                continue
            if counter == 13:
                batting_average.append(i)
                counter = counter + 1
                continue
            if counter == 14:
                on_base_percentage.append(i)
                counter = counter + 1
                continue
            if counter == 15:
                slugging_percentage.append(i)
                counter = counter + 1
                continue
            if counter == 16:
                on_base_plus_slugging.append(i)
                counter = 0
                continue
        print('Collected stats for season ' + str(year) + '; Page: ' + str(page))

data = {'season': season,
        'first_name': first_name, 
        'last_name': last_name,
        'link': link,
        'position': position,
        'team': team,
        'games_played': games_played,
        'at_bats': at_bats,
        'runs': runs,
        'hits': hits,
        'doubles': doubles,
        'triples': triples,
        'homeruns': homeruns,
        'rbi': rbi,
        'walks': walks,
        'strikeouts': strikeouts,
        'stolen_bases': stolen_bases,
        'caught_stealing': caught_stealing,
        'batting_average': batting_average,
        'on_base_percentage': on_base_percentage,
        'slugging_percentage': slugging_percentage,
        'on_base_plus_slugging': on_base_plus_slugging
        }

df = pd.DataFrame(data)
df.to_csv(r'C:\Users\Logan Custer\OneDrive - Utah Tech University\Courses\ISA 4060\Semster Project\mlb_season_data.csv', index=False)
print(len(df['link']))
