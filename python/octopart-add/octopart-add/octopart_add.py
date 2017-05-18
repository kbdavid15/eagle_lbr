import requests
import json
import time
import codecs

MAX_QUERIES_PER_REQUEST = 20
OCTOPART_API_KEY = ''


class Part():
    def __init__(self, part_match_result):
        self.part_match_result = part_match_result
        self.mpn = ""
        self.url = ""
        self.manufacturer = ""
        self.specs = {}
        self.process_result()

    def process_result(self):
        first_item = self.part_match_result['items'][0]
        self.mpn = first_item['mpn']
        self.url = first_item['octopart_url']
        self.manufacturer = first_item['manufacturer']['name']
        self.specs = first_item['specs']


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_api_key():
    global OCTOPART_API_KEY
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
    """Takes a list of mpn strings, and gets the specs from octopart. Returns dict of information"""
    match_url = "http://octopart.com/api/v3/parts/match?"
    results = []
    idx = 1
    for chunk in chunks(mpn_list, MAX_QUERIES_PER_REQUEST):
        print('Processing parts {} to {} of {}...'.format(idx, idx+len(chunk)-1, len(mpn_list)))
        idx += len(chunk)
        query = []
        for mpn in chunk:
            query.append({'mpn':mpn})

        params = {
            'queries':json.dumps(query),
            'apikey': get_api_key(),
            'include[]':'specs',
        }

        r = request_handle_timeout(match_url, params)
        if r.ok:
            response = r.json()
            for result in response['results']:
                results.append(result)  # type is PartsMatchResult object

    print("API requests complete")
    parts = [Part(p) for p in results]
    return parts


def output_parts_list(parts_list, out_file = "output.csv"):
    # get list of all possible keys
    key_list = []
    for part in parts_list:
        key_list += part.specs.keys()
    key_list = list(set(key_list))  # remove duplicates

    with open(out_file, 'w', encoding='utf16') as f:
        f.write('mpn\tmanufacturer\t')
        f.write('\t'.join(key_list) + '\n')
        for part in parts_list:
            f.write('\t'.join([part.mpn, part.manufacturer]) + '\t')
            for key in key_list:
                if key in part.specs.keys():
                    f.write(part.specs[key]['display_value'] + '\t')
                else:
                    f.write('\t')
            f.write('\n')


if __name__ == '__main__':
    mpn_test_list = ['RK73H1ET*3302F', 'RK73H1ET*4751F', 'RK73H1ET*3651F', 'RK73B1JT*824J', 'CRCW0603820KJN*', 'RK73H1ET*2552F', 'RK73H1ET*1213F', 'RK73B1ET*105J', 'RK73H2AT*2552F', 'RK73H1ET*33R0F', 'RK73H1ET*8061F', 'RK73H1ET*3321F', 'RK73H2AT*6651F', 'RK73H1ET*9310F', 'RK73H2AT*6491F', 'RK73H2AT*1001F', 'RK73B1ET*472J', 'CRCW04024K70JN*', 'RK73H1ET*1003F', 'RK73H1ET*9102F', 'RK73H1ET*2201F', 'RK73H1ET*4752F', 'CRCW040247K5FK*', 'RK73H2AT*2611F', 'RK73H1ET*1601F', 'RK73H1ET*6652F', 'RK73H1ET*1152F', 'RK73H1ET*2701F', 'CRCW04022K70FK*' ]

    spec_list = ['case_package', 'voltage_rating_dc', 'dielectric_characteristic', 'capacitance_tolerance', 'pin_count', 'capacitance']

    response = get_specs_from_octopart(mpn_test_list)

    # print mpn's
    print('Creating output file...')
    output_parts_list(response)
    print('Complete')