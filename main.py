import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import numpy as np


def volleyball():
    url = get_url('-volleyball/stats/')

    print("Would you like to look at team(T), offence(O), or defence(D) stats?")
    choice = input().strip().upper()

    while choice in ['O', 'D', 'T']:
        if choice == 'O':
            volley_offence(url)
        elif choice == 'D':
            volley_defence(url)
        elif choice == 'T':
            team_volley(url)
        print("Would you like to look at team(T), offence(O), defence(D), or exit?")
        choice = input().strip().upper()


def volley_offence(url):
    individual_keep_going = 'Y'
    while individual_keep_going == "Y":
        print("Would you like to look at overall stats or conference stats?")
        section = input().strip().upper()
        df = (volleyball_offence_stats(url, section[0]))
        stat_message()
        stat_loop(df, "eg. \"players with more than 30 PTS\" or \"player with the most SA/S\" "
                  "Otherwise, type X.")
        print('For more individual stats, type Y')
        individual_keep_going = input().strip().upper()


def volley_defence(url):
    individual_keep_going = 'Y'
    while individual_keep_going == "Y":
        print("Would you like to look at overall stats or conference stats?")
        section = input().strip().upper()
        df = (volleyball_defence_stats(url, section[0]))
        stat_loop(df, "eg. \"players with more than 30 BLK\" or \"player with the most BHE\" "
                  "Otherwise, type X.")
        print('For more individual stats, type Y')
        individual_keep_going = input().strip().upper()


def team_volley(url):
    team_keep_going = 'Y'
    while team_keep_going == "Y":
        df = (volleyball_team_stats(url))
        print(df)
        print('For more team stats, type Y')
        team_keep_going = input().strip().upper()


def volleyball_offence_stats(url, choice):
    section = 0
    if choice == "O":
        section = 1
    elif choice == "C":
        section = 3

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find_all('thead')
    player_offence_cols = headers[1]
    table_headers = [header.text.strip() for header in player_offence_cols
                     if header.get_text(strip=True)][1]
    table_headers = table_headers.split('\n')
    df = pd.DataFrame(columns=table_headers)

    body = soup.find_all('tbody')
    player_offence_stats = body[section]

    for row in player_offence_stats.find_all('tr'):
        if isinstance(row, Tag):
            data = row.find_all('td')
            data = [col.get_text(strip=True) for col in data]
            data = data[1:-1]
            length = len(df)
            df.loc[length] = data

    df = df.set_index(pd.Index(range(1, len(df) + 1)))
    for col in df.columns:
        if col != "Player":
            df[col] = df[col].astype(float)
    df = clean_name(df)
    df = df.rename_axis("#")

    return df


def volleyball_defence_stats(url, choice):
    section = 0
    if choice == "O":
        section = 2
    elif choice == "C":
        section = 4

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find_all('thead')
    player_defence_cols = headers[2]
    table_headers = [header.text.strip() for header in player_defence_cols
                     if header.get_text(strip=True)]
    table_headers = table_headers[0].split('\n')[3:3] + table_headers[1].split('\n')
    df = pd.DataFrame(columns=table_headers)

    body = soup.find_all('tbody')
    player_defence_stats = body[section]
    for row in player_defence_stats.find_all('tr'):
        if isinstance(row, Tag):
            data = row.find_all('td')
            data = [col.get_text(strip=True) for col in data]
            data = data[1:-1]
            length = len(df)
            df.loc[length] = data

    df = df.set_index(pd.Index(range(1, len(df) + 1)))
    for col in df.columns:
        if col != "Player":
            df[col] = df[col].astype(float)
    df = clean_name(df)
    df = df.rename_axis("#")

    return df


def volleyball_team_stats(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find_all('span', class_="hide-on-medium")
    table_headers = [header.text.strip() for header in headers
                     if header.get_text(strip=True)][1:]
    df = pd.DataFrame(columns=['Home', 'Opponents'], index=table_headers)

    body = soup.find_all('tbody')
    team_stats = body[0]

    i = 0
    for row in team_stats.find_all('tr'):
        if isinstance(row, Tag):
            data = row.find_all('td')
            data = [col.get_text(strip=True) for col in data][1:]
            if not data:
                continue
            df.iloc[i] = data
            i += 1

    for col in df.columns:
        df[col] = df[col].astype(float)

    return df


def soccer():
    url = get_url('-soccer/stats/')
    print("Would you like to look at team(T), offence(O), or goalie(G) stats?")
    choice = input().strip().upper()
    while choice in ['O', 'G', 'T']:
        if choice == 'O':
            soccer_offence(url)
        elif choice == 'G':
            soccer_goalies(url)
        elif choice == 'T':
            team_soccer(url)
        print("Would you like to look at team(T), offence(O), or goalie(G) stats?")
        choice = input().strip().upper()


def soccer_offence(url):
    individual_keep_going = 'Y'
    while individual_keep_going == "Y":
        print("Would you like to look at overall stats or conference stats?")
        section = input().strip().upper()
        df = (soccer_offence_stats(url, section[0]))
        stat_loop(df, "eg. \"players with more than 5 G\" or \"player with the most A\" "
                  "Otherwise, type X.")
        print('For more individual stats, type Y')
        individual_keep_going = input().strip().upper()


def soccer_goalies(url):
    individual_keep_going = 'Y'
    while individual_keep_going == "Y":
        print("Would you like to look at overall stats or conference stats?")
        section = input().strip().upper()
        df = (soccer_goalie_stats(url, section[0]))
        stat_loop(df, "eg. \"players with more than 10 GS\" or \"player with the highest SV%\" "
                  "Otherwise, type X.")
        print('For more individual stats, type Y')
        individual_keep_going = input().strip().upper()


def team_soccer(url):
    team_keep_going = 'Y'
    while team_keep_going == "Y":
        df = (soccer_team_stats(url))
        print(df)
        print('For more team stats, type Y')
        team_keep_going = input().strip().upper()


def soccer_offence_stats(url, choice):
    section = 0
    if choice == "O":
        section = 1
    elif choice == "C":
        section = 3
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find_all('thead')
    player_offence_cols = headers[1]
    table_headers = [header.text.strip() for header in player_offence_cols
                     if header.get_text(strip=True)][0]
    table_headers = table_headers.split('\n')

    df = pd.DataFrame(columns=table_headers)
    df = df.drop(columns="Bio Link")
    body = soup.find_all('tbody')
    player_offence_stats = body[section]

    for row in player_offence_stats.find_all('tr'):
        if isinstance(row, Tag):
            data = row.find_all('td')
            data = [col.get_text(strip=True) for col in data]
            data = data[:-1]
            if data[1] == "TeamTMTeam":
                continue
            length = len(df)
            df.loc[length] = data

    df = df.set_index('#')
    for col in df.columns:
        if col not in ["Player", "YC-RC", "PG-PA"]:
            df[col] = df[col].astype(float)
    df = clean_name(df)

    return df


def soccer_goalie_stats(url, choice):
    section = 0
    if choice == "O":
        section = 2
    elif choice == "C":
        section = 4
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find_all('thead')
    player_offence_cols = headers[2]
    table_headers = [header.text.strip() for header in player_offence_cols
                     if header.get_text(strip=True)][0]
    table_headers = table_headers.split('\n')

    df = pd.DataFrame(columns=table_headers)
    df = df.drop(columns="Bio Link")
    body = soup.find_all('tbody')
    player_offence_stats = body[section]

    for row in player_offence_stats.find_all('tr'):
        if isinstance(row, Tag):
            data = row.find_all('td')
            data = [col.get_text(strip=True) for col in data]
            data = data[:-1]
            if data[1] == "TeamTMTeam":
                continue
            length = len(df)
            df.loc[length] = data

    df = df.set_index('#')
    df['MIN'] = df['MIN'].str.replace(':', '.')
    for col in df.columns:
        if col not in ["SHO/CBO", "Player"]:
            df[col] = df[col].astype(float)
    df = clean_name(df)

    return df


def soccer_team_stats(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find_all('span', class_="hide-on-medium")
    table_headers = [header.text.strip() for header in headers
                     if header.get_text(strip=True)][1:]
    df = pd.DataFrame(columns=['Home', 'Opponents'], index=table_headers)

    body = soup.find_all('tbody')
    team_stats = body[0]

    i = 0
    for row in team_stats.find_all('tr'):
        if isinstance(row, Tag):
            data = row.find_all('td')
            data = [col.get_text(strip=True) for col in data][1:]
            if not data:
                continue
            df.iloc[i] = data
            i += 1
    print(df)
    for row in df.index:
        if row in ["SOG", "PG-PA"]:
            continue
        df.loc[row] = df.loc[row].astype(float)

    return df


def football():
    print("Nothing to see here...\n")


def basketball():
    print("Nothing to see here...")


def baseball():
    print("Nothing to see here...")


def hockey():
    print("Which draft year would you like to see a description of?\n")
    year = input().strip()
    draft = draft_data('https://www.hockey-reference.com/draft/NHL_' + year + '_entry.html')
    print(draft.describe().T)


def draft_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    headers = soup.find('thead')
    headers = headers.find_all("th")
    table_headers = [header.text.strip() for header in headers
                     if header.get_text(strip=True) and
                     not ('over_header' in header.get('class', []))]
    df = pd.DataFrame(columns=table_headers)
    df = df.drop(columns='Overall')

    body = soup.find('tbody')
    body = body.find_all('tr')
    for row in body:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        if any(individual_row_data):
            length = len(df)
            df.loc[length] = individual_row_data

    df = df.set_index(pd.Index(range(1, len(df) + 1)))
    df = df.replace('', np.nan)
    for col in df.columns:
        if col not in ["Team", "Player", "Nat.", "Pos", "Amateur Team"]:
            df[col] = df[col].astype(float)
    return df


def stat_message():
    print("For a specific player summary, type P followed by their last name. "
          "For a specific stat summary, type S followed by the stat you'd like. ")
    print("For conditional search, type C followed by what you'd like to search for, ", end="")


def stat_loop(df, message):
    print(df.describe().T)
    print("For a specific player summary, type P followed by their last name. "
          "For a specific stat summary, type S followed by the stat you'd like. ")
    print("For conditional search, type C followed by what you'd like to search for, ", end="")
    print(message)
    second_keep_going = input().strip().upper()
    while second_keep_going in ['C', 'S', 'P', 'Y']:
        stat_handler(df, second_keep_going)
        print("For a specific player summary, type P followed by their last name. "
              "For a specific stat summary, type S followed by the stat you'd like. ")
        print("For conditional search, type C followed by what you'd like to search for, ", end="")
        print(message)
        second_keep_going = input().strip().upper()


def stat_handler(df, second_choice):
    if second_choice == 'P':
        player_summary(df, input().strip())
    elif second_choice == 'S':
        stat_summary(df, input().strip().upper())
    elif second_choice == 'C':
        conditional_search(df, input().upper())


def stat_summary(df, stat):
    # while stat not in df.columns:
    #     print("Name does not match database. Please enter a valid name")
    #     stat = input()
    print(df.loc[:, stat].describe())


def player_summary(df, player):
    print(df[df.LastName == player].T)


def conditional_search(df, user_input):
    condition = find_condition(user_input)
    stat = find_stat(df, user_input)
    num = find_num(user_input)
    if condition == 'MAX':
        print((df[df[stat] == df[stat].max()][['FirstName', 'LastName', stat]]))
    elif condition == 'MIN':
        print((df[df[stat] == df[stat].min()][['FirstName', 'LastName', stat]]))
    elif condition == 'GREATER':
        print(df.loc[df[stat] > num].T)
    elif condition == 'LESS':
        print(df.loc[df[stat] < num].T)


def find_condition(user_input):
    condition = 'X'
    user_input = user_input.split(' ')
    if any(word in ['MAX', 'MOST', 'HIGHEST', 'LARGEST', 'GREATEST'] for word in user_input):
        condition = 'MAX'
    elif any(word in ['MIN', 'LEAST', 'LOWEST', 'SMALLEST'] for word in user_input):
        condition = 'MIN'
    elif any(word in ['GREATER', 'MORE', 'LARGER', 'BIGGER', 'HIGHER'] for word in user_input):
        condition = 'GREATER'
    elif any(word in ['LESS', 'SMALLER', 'LOWER', 'FEWER'] for word in user_input):
        condition = 'LESS'
    else:
        print("Error: invalid input.")

    return condition


def find_stat(df, user_input):
    user_input = user_input.split(' ')
    stat = None
    for word in user_input:
        if word in df.columns:
            stat = word

    if stat == ' ':
        print("Error: invalid input.")
    return stat


def find_num(user_input):
    num = ''
    for char in user_input:
        if char.isdigit():
            num += char
    if num == '':
        return num
    return int(num)


def get_url(sport):
    school = get_school()

    if school == 'tufts':
        year = get_year()
        gender = get_gender(sport)
        return 'https://gotuftsjumbos.com/sports/' + gender + sport + year

    return school


def get_year():
    print("Which year would you like to look at? "
          "Enter the first year of the season (eg. for 2023/24, enter 2023)")
    year = input().strip()
    return year


def get_school():
    print("Which school would you like to look at? "
          "If tufts, type tufts. "
          "Otherwise, copy and paste the stats page of the school you want")
    return input().lower()


def get_gender(sport):
    if sport == '-volleyball/stats/':
        return 'womens'
    if sport == '-football/stats/':
        return 'mens'
    else:
        print("Mens or womens?")
        return input().strip().lower()


def clean_name(df):
    saved = df.index
    df = df.reset_index(drop=True)

    for i in range(len(df)):
        parts = (df.iloc[i, 0]).split(',')
        df.loc[i, 'LastName'] = parts[0].strip()
        df.loc[i, 'FirstName'] = parts[2].strip()

    df = df.drop(columns="Player")
    df.set_index(saved, inplace=True)
    return df


def prompt_and_execute():
    print("Enter the first letter of the sport you're looking for, "
          "BB for basketball, or any other input to end your session")
    choice = input().strip().upper()

    while choice in ["H", 'V', 'S', 'F', 'B', 'BB']:
        if choice == "H":
            hockey()
        elif choice == 'V':
            volleyball()
        elif choice == 'S':
            soccer()
        elif choice == 'F':
            football()
        elif choice == 'B':
            baseball()
        elif choice == 'BB':
            basketball()

        print("Enter the first letter of the sport you're looking for, "
              "BB for basketball, or any other input to end your session")
        choice = input().strip().upper()


print("Hi, I'm Statbot!")
prompt_and_execute()
