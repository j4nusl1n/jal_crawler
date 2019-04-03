# encoding: utf-8

import requests

def get_html_by_flight(airline_code, flight_no, date=None):
    endpoint = 'http://fltinfo.5971.jal.co.jp/rsv/ArrivalAndDepartureFlightNameInfo_en.do'
    params = {
        'airlineCode': airline_code,
        'flightSerNo': '{:03d}'.format(flight_no),
        'dateAttribute': None,
        'fromScreen': True
    }
    
    if date is not None:
        if date in ['1', '2', 1, 2]:
            params['dateAttribute'] = str(date)

    resp = requests.get(endpoint, params=params)
    return resp

if __name__ == "__main__":
    resp = get_html_by_flight('JTA', 3537, date=1)
    print(resp)
    print(resp.text)
    print(resp.request.url)
    with open('test_default.html', 'w') as f:
        f.write(resp.text)