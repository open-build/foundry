import requests
import pandas as pd

# Define your API keys here
CRUNCHBASE_API_KEY = ''
ANGELLIST_API_KEY = ''
PRODUCTHUNT_API_KEY = ''
CLEARBIT_API_KEY = ''

# Define functions to get data from each API
def get_crunchbase_data():
    url = 'https://api.crunchbase.com/v3.1/organizations'
    params = {
        'user_key': CRUNCHBASE_API_KEY,
        'locations': 'worldwide',
        'page': 1,
        'sort_order': 'updated_at DESC'
    }
    response = requests.get(url, params=params)
    data = response.json()['data']['items']
    results = []
    for item in data:
        results.append({
            'name': item['properties']['name'],
            'description': item['properties']['short_description'],
            'stage': item['properties']['funding_stage'],
            'founders': ', '.join([founder['name'] for founder in item['relationships']['founders']['items']])
        })
    return results

def get_angellist_data():
    url = 'https://api.angel.co/1/startups'
    params = {
        'access_token': ANGELLIST_API_KEY,
        'filter': 'raising'
    }
    response = requests.get(url, params=params)
    data = response.json()['startups']
    results = []
    for item in data:
        results.append({
            'name': item['name'],
            'description': item['high_concept'],
            'stage': item['company_stage'],
            'founders': ', '.join([founder['name'] for founder in item['founders']])
        })
    return results

def get_producthunt_data():
    url = 'https://api.producthunt.com/v2/api/graphql'
    query = """
    {
      posts(order: RANKING) {
        edges {
          node {
            name
            tagline
            makers {
              name
            }
          }
        }
      }
    }
    """
    headers = {
        'Authorization': f'Bearer {PRODUCTHUNT_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json={'query': query}, headers=headers)
    data = response.json()['data']['posts']['edges']
    results = []
    for item in data:
        results.append({
            'name': item['node']['name'],
            'description': item['node']['tagline'],
            'stage': 'N/A',
            'founders': ', '.join([maker['name'] for maker in item['node']['makers']])
        })
    return results

def get_clearbit_data():
    url = 'https://company.clearbit.com/v2/companies/find'
    params = {
        'sort_order': 'created_at:desc'
    }
    headers = {
        'Authorization': f'Bearer {CLEARBIT_API_KEY}'
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    results = []
    for item in data:
        results.append({
            'name': item['name'],
            'description': item['description'],
            'stage': 'N/A',
            'founders': ', '.join([founder['name'] for founder in item['founders']])
        })
    return results

# Fetch data from each API
crunchbase_data = get_crunchbase_data() if CRUNCHBASE_API_KEY else []
angellist_data = get_angellist_data() if ANGELLIST_API_KEY else []
producthunt_data = get_producthunt_data() if PRODUCTHUNT_API_KEY else []
clearbit_data = get_clearbit_data() if CLEARBIT_API_KEY else []

# Combine all data into a single DataFrame
combined_data = crunchbase_data + angellist_data + producthunt_data + clearbit_data
df = pd.DataFrame(combined_data)

# Save to CSV or any format needed for training
df.to_csv('startup_data.csv', index=False)

print('Data saved to startup_data.csv')
