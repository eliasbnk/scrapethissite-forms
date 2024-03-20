import json
import requests
from bs4 import BeautifulSoup


def fetch_team_data(base_url, params={}):

    parameters = params.copy()

    if 'per_page' not in parameters or parameters['per_page'] not in {'25', '50', '100'}:

        parameters['per_page'] = '100'

    response = requests.get(base_url, params=parameters)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    team_tr = soup.select_one('tr.team')

    if not team_tr:
        return None

    soup_list = [soup]

    if 'page_num' in params or not params:
        return soup_list

    page_num = 2

    while True:

        parameters['page_num'] = page_num

        response = requests.get(base_url, params=parameters)

        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        team_tr = soup.select('tr.team')

        if team_tr:
            soup_list.append(soup)
            if len(team_tr) == parameters['per_page']:
                page_num += 1
            else:
                break
        else:
            break

    return soup_list


def extract_team_data(soup):
    team_trs = soup.select('tr.team')

    team_data = []

    for team_tr in team_trs:

        name = team_tr.select_one('td.name').text.strip()
        year = team_tr.select_one('td.year').text.strip()
        wins = team_tr.select_one('td.wins').text.strip()
        losses = team_tr.select_one('td.losses').text.strip()
        ot_losses = team_tr.select_one('td.ot-losses').text.strip()
        win_pct = team_tr.select_one('td.pct').text.strip()
        goals_for = team_tr.select_one('td.gf').text.strip()
        goals_against = team_tr.select_one('td.ga').text.strip()
        goal_difference = team_tr.select_one('td.diff').text.strip()

        team_data.append({
            'team_name': name,
            'year': year,
            'wins': wins,
            'losses': losses,
            'ot_losses': ot_losses,
            'win_pct': win_pct,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goal_difference
        })

    return team_data


if __name__ == "__main__":

    base_url = 'https://www.scrapethissite.com/pages/forms/'

    team_data = []

    params = {'q': 'boston', 'page_num': '12'}

    team_soups = fetch_team_data(base_url, params=params)

    if team_soups:

        for team_soup in team_soups:

            team_data.extend(extract_team_data(team_soup))

        print(json.dumps(team_data[:25], indent=4))

    else:

        print('An error occurred')
