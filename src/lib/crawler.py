# encoding: utf-8

import requests

_FLIGHT_INFO_DOMAIN = 'http://fltinfo.5971.jal.co.jp'

def get_flight_status_html(airline_code, flight_no, date=None):
    endpoint = '/rsv/ArrivalAndDepartureFlightNameInfo_en.do'
    params = {
        'airlineCode': airline_code,
        'flightSerNo': '{:03d}'.format(flight_no),
        'dateAttribute': None,
        'fromScreen': True
    }

    if date is not None:
        if date in ['1', '2', 1, 2]:
            params['dateAttribute'] = str(date)

    resp = requests.get(
        '{}{}'.format(_FLIGHT_INFO_DOMAIN, endpoint),
        params=params
    )
    return resp

def get_status_html_by_dep_arr(departure, arrival, date=None):
    """Get flights' status by departure and arrival airport code
    
    Arguments:
        departure {str} -- IATA code of departure airport
        arrival {str} -- IATA code of arrival airport
    
    Keyword Arguments:
        date {int} --   If set to 1, this function will fetch the html of yesterday. 
                        If set to 2, this function will fetch the html of tomorrow 
                        (default: {None})
    """
    endpoint = '/rsv/ArrivalAndDepartureSectionInfo_en.do'
    params = {
        'DPORT': departure,
        'APORT': arrival,
        'DATEFLG': None
    }

    if date is not None:
        if date in [1, 2, '1', '2']:
            params['DATEFLG'] = date

    resp = requests.get(
        '{}{}'.format(_FLIGHT_INFO_DOMAIN, endpoint),
        params=params
    )

    return resp

def get_section_miles(departure, arrival):
    domain = 'http://www121.jal.co.jp'
    endpoint = '/JmbWeb/JR/SectionMileCalc_en.do'
    params = {
        'dep1': departure,
        'arr1': arrival,
    }

    resp = requests.get(
        '{}{}'.format(domain, endpoint),
        params=params
    )
    return resp

if __name__ == "__main__":
    # resp = get_section_miles('TYO', 'GAJ')
    # print(resp)
    # print(resp.text)
    # resp = get_flight_status_html('JAL', 904, date=1)
    resp = get_status_html_by_dep_arr('HND', 'OKA', date=1)
    print(resp)
    print(resp.text)
    # print(resp.request.url)
    # with open('test_default.html', 'w') as f:
    #     f.write(resp.text)
