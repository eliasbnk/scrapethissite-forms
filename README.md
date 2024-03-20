# Hockey Teams: Forms, Searching and Pagination - Walkthrough
> walkthrough for the web-scrapping exercise found on https://www.scrapethissite.com
## Step 0: Install necessary dependencies
### - Step 0.1: Create a virtual environment:
```bash 
python -m venv venv
```


### - Step 0.2: Activate the virtual environment:

***Windows***:	
```bash
venv\Scripts\activate
```

***Mac/Linux***:
```bash
source venv/bin/activate
```
### - Step 0.3: Install dependencies:
```bash
pip install requests beautifulsoup4
```
* * *
## Step 1: Get the Webpage HTML
Start by fetching the HTML content of the target webpage. We'll use the `requests` library to do this.

```python
import requests

# Define the URL of the webpage
url = 'https://www.scrapethissite.com/pages/forms/'

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Extract the HTML content from the response
html_content = response.text
```
* * *
## Step 2: Spot HTML Patterns

Inspect the HTML structure for any recurring patterns. It appears that each team's data is contained within `<tr>` elements having the class ``"team"``.

```html
<tr class="team">
    <td class="name">
        Boston Bruins
    </td>
    <td class="year">
        1990
    </td>
    <td class="wins">
        44
    </td>
    <td class="losses">
        24
    </td>
    <td class="ot-losses">
    </td>
    <td class="pct text-success">
        0.55
    </td>
    <td class="gf">
        299
    </td>
    <td class="ga">
        264
    </td>
    <td class="diff text-success">
        35
    </td>
</tr>

<tr class="team">
    <td class="name">
        Buffalo Sabres
    </td>
    <td class="year">
        1990
    </td>
    <td class="wins">
        31
    </td>
    <td class="losses">
        30
    </td>
    <td class="ot-losses">
    </td>
    <td class="pct text-danger">
        0.388
    </td>
    <td class="gf">
        292
    </td>
    <td class="ga">
        278
    </td>
    <td class="diff text-success">
        14
    </td>
</tr>
<!--.col-->
```
* * *
## Step 3: Parse the HTML

We'll use ``BeautifulSoup``, to parse the HTML content and make it ready for extraction.

```python
from bs4 import BeautifulSoup

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')
```
* * *
## Step 4: Extract the Data

Having identified the pattern, we can gather all `<tr>` elements with the class ``"team"`` as individual datasets. Then, we'll loop through each dataset and extract details like name, wins, losses, etc...

```python
# Find all <tr> elements with the class "team"
team_trs = soup.select('tr.team')

# Iterate through each <tr> element for data extraction
for team_tr in team_trs:

    # Extract Team Name
    name = team_tr.select_one('td.name')

    # gets:

    # <td class="name">
    #     Boston Bruins
    # </td>
  

    # We only need the text:

    name = name.text

    # returns:

    # Boston Bruins

    # But with extra whitespace

    # We can remove the extra whitespace:

    name = name.strip()

    # returns:

    # Boston Bruins

    # Without any extra whitespace

    # We can achieve clean text extraction in a single line by appending the .text.strip() methods.
    # For example, to extract the year, we can write:

    # Extract Year
    year = team_tr.select_one('td.year').text.strip()

    # This line not only selects the year element but also extracts its text content
    # and removes any leading or trailing whitespace, ensuring clean and properly formatted data.

    # Extract Wins
    wins = team_tr.select_one('td.wins').text.strip()
    
    # Extract Losses
    losses = team_tr.select_one('td.losses').text.strip()
    
    # Extract OT Losses
    ot_losses = team_tr.select_one('td.ot-losses').text.strip()
    
    # Extract Win %
    win_pct = team_tr.select_one('td.pct').text.strip()
    
    # Extract Goals For
    goals_for = team_tr.select_one('td.gf').text.strip()
    
    # Extract Goals Against
    goals_against = team_tr.select_one('td.ga').text.strip()
    
    # Extract Goal Difference
    goal_difference = team_tr.select_one('td.diff').text.strip()
```

* * *
### Put it all together:
```python
import json  # optional, added for output formating
import requests
from bs4 import BeautifulSoup

url = 'https://www.scrapethissite.com/pages/forms/'

response = requests.get(url)

html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

team_trs = soup.select('tr.team')

team_data = []

# note [:5], only will extract first 5 countries
for team_tr in team_trs[:5]:
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

# you can just do:
# print(team_data)

# but this will output the team_data, with indentation
print(json.dumps(team_data, indent=4))

```
### Outputs:
```json
[
    {
        "team_name": "Boston Bruins",
        "year": "1990",
        "wins": "44",
        "losses": "24",
        "ot_losses": "",
        "win_pct": "0.55",
        "goals_for": "299",
        "goals_against": "264",
        "goal_difference": "35"
    },
    {
        "team_name": "Buffalo Sabres",
        "year": "1990",
        "wins": "31",
        "losses": "30",
        "ot_losses": "",
        "win_pct": "0.388",
        "goals_for": "292",
        "goals_against": "278",
        "goal_difference": "14"
    },
    {
        "team_name": "Calgary Flames",
        "year": "1990",
        "wins": "46",
        "losses": "26",
        "ot_losses": "",
        "win_pct": "0.575",
        "goals_for": "344",
        "goals_against": "263",
        "goal_difference": "81"
    },
    {
        "team_name": "Chicago Blackhawks",
        "year": "1990",
        "wins": "49",
        "losses": "23",
        "ot_losses": "",
        "win_pct": "0.613",
        "goals_for": "284",
        "goals_against": "211",
        "goal_difference": "73"
    },
    {
        "team_name": "Detroit Red Wings",
        "year": "1990",
        "wins": "34",
        "losses": "38",
        "ot_losses": "",
        "win_pct": "0.425",
        "goals_for": "273",
        "goals_against": "298",
        "goal_difference": "-25"
    }
]
```
***
## This is only 1/3 of what we need to do
- [x] Fetch data from the first page.
- [ ] Fetch data from all or a specific page.
- [ ] Fetch data for a queried team name.

### Understanding Query Parameters

Our base URL is: `https://www.scrapethissite.com/pages/forms/`

To modify the behavior of data retrieval, you can append the following parameters to the base URL:

- `per_page=[25, 50, 100]`: Specifies the number of items per page.
- `page_num=[1...24]` at 25 per page (default):
  - Example: `?page_num=25&per_page=25` or `?page_num=25`
- `page_num=[1...12]` at 50 per page:
  - Example: `?page_num=12&per_page=50`
- `page_num=[1...6]` at 100 per page:
  - Example: `?page_num=6&per_page=100`
- `q=""` to query for a specific team:
  - Example: `q=boston`
***

## Step 1: Break code up into reusable modules 
### (separation of concerns)
```python
def fetch_team_data(url):
    response = requests.get(url)
    
    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup



def extract_team_data(soup):    
    team_trs = soup.select('tr.team')
    
    team_data = []
    
    for team_tr in team_trs[:5]:
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
```

### Modification we can do to `fetch_team_data`:

```python
def fetch_team_data(base_url, params={}):
    
    # Initialize parameters with the given params
    parameters = params.copy()
    
    # If 'per_page' is not provided, set it to 100; to minimize requests
    if 'per_page' not in parameters:
        parameters['per_page'] = '100'

    # Send a GET request to fetch the webpage content
    response = requests.get(base_url, params=parameters)

    # Extract the HTML content from the response
    html_content = response.text

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty list to store parsed soup objects
    soup_list = [soup]

    # If 'page_num' is provided or params is empty, return the parsed soup
    if 'page_num' in params or not params:
        return soup_list

    # Initialize page number
    page_num = 2  # Start from the second page

    # Loop to fetch data from subsequent pages
    while True:
        # Update page number in parameters
        parameters['page_num'] = page_num
        
        # Send a GET request with updated parameters
        response = requests.get(base_url, params=parameters)

        # Extract the HTML content from the response
        html_content = response.text

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Select a team row from the parsed HTML
        team_tr = soup.select_one('tr.team')

        # If a team row is found, append the parsed soup object to soup_list and increment page number
        if team_tr:
            soup_list.append(soup)
            page_num += 1
        else:
            # If no team row is found, break out of the loop
            break

    return soup_list
```

### Then all we need to do:

```python
# Define the base URL for fetching data
base_url = 'https://www.scrapethissite.com/pages/forms/'

# Initialize an empty list to store extracted team data
team_data = []

# Define optional parameters for the request
params = {'q': 'sharks', 'per_page': '25', 'page_num':'1'}

# Fetch HTML content for each page of the request
team_soups = fetch_team_data(base_url, params=params)

# Extract data from each page
for team_soup in team_soups:
    team_data.extend(extract_team_data(team_soup))

# Output (first 5, note [:5]) the extracted data with indentation
print(json.dumps(team_data[:5], indent=4))
```
### Output:
```json
[
    {
        "team_name": "San Jose Sharks",
        "year": "1991",
        "wins": "17",
        "losses": "58",
        "ot_losses": "",
        "win_pct": "0.212",
        "goals_for": "219",
        "goals_against": "359",
        "goal_difference": "-140"
    },
    {
        "team_name": "San Jose Sharks",
        "year": "1992",
        "wins": "11",
        "losses": "71",
        "ot_losses": "",
        "win_pct": "0.131",
        "goals_for": "218",
        "goals_against": "414",
        "goal_difference": "-196"
    },
    {
        "team_name": "San Jose Sharks",
        "year": "1993",
        "wins": "33",
        "losses": "35",
        "ot_losses": "",
        "win_pct": "0.393",
        "goals_for": "252",
        "goals_against": "265",
        "goal_difference": "-13"
    },
    {
        "team_name": "San Jose Sharks",
        "year": "1994",
        "wins": "19",
        "losses": "25",
        "ot_losses": "",
        "win_pct": "0.396",
        "goals_for": "129",
        "goals_against": "161",
        "goal_difference": "-32"
    },
    {
        "team_name": "San Jose Sharks",
        "year": "1995",
        "wins": "20",
        "losses": "55",
        "ot_losses": "",
        "win_pct": "0.244",
        "goals_for": "252",
        "goals_against": "357",
        "goal_difference": "-105"
    }
]
```
**One thing to consider is error boundary/exceptions...**
**As user can provide a page that doesn't have content,**
**Or provide an invalid per_page number.**

### Basic Error Boundary:
```python
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

...


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
```
