import requests
import json
import time

MAX_QUERIES_PER_REQUEST = 20
OCTOPART_API_KEY = ''

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_api_key():
    if OCTOPART_API_KEY == '':
        with open('key.txt') as f:
            content = f.readlines()
        OCTOPART_API_KEY = content[0]
    return OCTOPART_API_KEY

def request_handle_timeout(url, params):
    retry_count = 0
    while retry_count < 3:
        r = requests.get(url, params)
        if r.status_code == 200:
            break
        elif r.status_code == 429:
            time.sleep(1)   # wait 1 second, exceeded 3 api calls/second
        retry_count += 1
    return r

def get_specs_from_octopart(mpn_list):
    "Takes a list of mpn strings, and gets the specs from octopart. Returns dict of information"
    match_url = 'http://octopart.com/api/v3/parts/match?'
    results = []
    for chunk in chunks(mpn_list, MAX_QUERIES_PER_REQUEST):
        query = []
        for mpn in chunk:
            query.append({'mpn':mpn})

        params = {
            'queries':json.dumps(query),
            'apikey': get_api_key(),
            'include[]':'specs',
        }

        r = request_handle_timeout(url, params)
        if r.ok:
            response = r.json()
            for result in response['results']:
                results.append(result)  # type is PartsMatchResult object

    return results

if __name__ == '__main__':
    url = 'http://octopart.com/api/v3/parts/match?'

    mpn = '04025A560FAT2A'
    mpn_test_list = ['RK73H1ET*3302F', 'RK73H1ET*4751F', 'RK73H1ET*3651F', 'RK73B1JT*824J', 'CRCW0603820KJN*', 'RK73H1ET*2552F', 'RK73H1ET*1213F', 'RK73B1ET*105J', 'RK73H2AT*2552F', 'RK73H1ET*33R0F', 'RK73H1ET*8061F', 'RK73H1ET*3321F', 'RK73H2AT*6651F', 'RK73H1ET*9310F', 'RK73H2AT*6491F', 'RK73H2AT*1001F', 'RK73B1ET*472J', 'CRCW04024K70JN*', 'RK73H1ET*1003F', 'RK73H1ET*9102F', 'RK73H1ET*2201F', 'RK73H1ET*4752F', 'CRCW040247K5FK*', 'RK73H2AT*2611F', 'RK73H1ET*1601F', 'RK73H1ET*6652F', 'RK73H1ET*1152F', 'RK73H1ET*2701F', 'CRCW04022K70FK*' ]

    spec_list = ['case_package', 'voltage_rating_dc', 'dielectric_characteristic', 'capacitance_tolerance', 'pin_count', 'capacitance']

    response = get_specs_from_octopart(mpn_test_list)


    # print mpn's
    for part in response:
        for item in part['items']:
            print(item['mpn'])
            for spec, value in item['specs']:
                print(spec + ' ' + item['specs'][spec]['display_value'])
            break


