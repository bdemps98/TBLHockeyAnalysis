from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd
import datetime as dt

# Data points that are being scraped
DATA_POINTS = ['player', 'age', 'pos', 'games_played', 'goals', 'assists', 'points', 'plus_minus', 'pen_min']

# The year in which the Tampa Bay Lightning were founded
FOUNDED = 1993

# The team in which we are aquiring the data from
TEAM = 'TBL'

# Used to get the current year
today = dt.datetime.now()

def scrape_player_data(year):
    # If the year being tried is the current year the url needs to default because of the website structure
    url = (lambda year: f"https://www.hockey-reference.com/teams/{TEAM}/{year}.html"
           if year != today.year else f"https://www.hockey-reference.com/teams/{TEAM}/")(year)
    response = rq.get(url)
    html_content = response.content

    # Beautiful Soup object
    soup = bs(html_content, 'html.parser')

    # Find all <tr> elements
    player_rows = soup.find_all('tr')

    data = {data_point: [] for data_point in DATA_POINTS}

    for player_row in player_rows:
        try:
            player_name = player_row.find('td', {'data-stat': 'player'})
            if player_name:
                for data_point in DATA_POINTS:
                    data_value = player_row.find('td', {'data-stat': data_point})
                    data[data_point].append(data_value.get_text(strip=True) if data_value else '0')
        except AttributeError:
            continue

    # Check that all lists have the same length
    data_lengths = [len(data[data_point]) for data_point in DATA_POINTS]
    if not all(length == data_lengths[0] for length in data_lengths):
        print(f"Data inconsistency for year {year}.")
    
    df = pd.DataFrame(data)
    return df

# Generates a list from the year they were founded to the current year.
years = [str(year) for year in range(FOUNDED, today.year + 1)]

# Creates the Excel Writer object
excel_file = pd.ExcelWriter('player_data.xlsx', engine='xlsxwriter')

for year in years:
    df = scrape_player_data(year)
    df.to_excel(excel_file, sheet_name=year, index=False)

excel_file.close()

# Confirms completion of the web scrape
print("Player data has been saved to 'player_data.xlsx'.")
