import requests
import json

url = 'http://octopart.com/api/v3/parts/match?'

mpn = '04025A560FAT2A'

query = [{'mpn':mpn}]

params = {
    'queries':json.dumps(query),
    'apikey':'0c9d5f73',
    'include[]':'specs',
}

spec_list = ['case_package', 'voltage_rating_dc', 'dielectric_characteristic', 'capacitance_tolerance', 'pin_count', 'capacitance']


r = requests.get(url, params)
response = r.json()

print(response['msec'])

# print mpn's
for result in response['results']:
    for item in result['items']:
        print(item['mpn'])
        for spec in item['specs']:
            print(spec)
    break