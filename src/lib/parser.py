# encoding: utf-8

from lxml import etree
import re

class DomesticStatus(object):
    _time_table = None
    def __init__(self, page_str=None):
        if type(page_str) is not str:
            raise TypeError(
                'Expecting type "str", instead {} given'.format(type(page_str))
            )
        self.page_str = page_str
        self.parse()

    def parse(self):
        self.page_tree = etree.HTML(
            self.page_str, 
            parser=etree.HTMLParser(remove_comments=True, remove_blank_text=True)
        )

        if self.hasError():
            error_message = 'PageError'
            if len(self.error_messages):
                error_message = '{}: {}'.format(error_message, ', '.join(self.error_messages))
            raise Exception(error_message)

        time_table = self.getTimeTable()
        if time_table is None:
            raise Exception('ParseError')

        self._time_table = time_table

    def hasError(self):
        self.error_messages = []
        if len(self.page_tree.xpath('//div[@class="errorMessageBlockA01"]')):
            error_nodes = self.page_tree.xpath('//div[@class="errorMessageBlockA01"]')
            for node in error_nodes:
                for line in node.xpath('//ul//li'):
                    if type(line.text) is str:
                        self.error_messages.append(line.text.strip())

            return True

        return False

    def getTimeTable(self):
        if self._time_table is not None:
            return self._time_table

        node_list = self.page_tree.xpath('//div[@id="completedTable-body"]//table')
        if len(node_list):
            return node_list[0]
        
        return None

    def parseTimeTable(self, time_table=None):
        if time_table is None:
            time_table = self._time_table
        dict_time = {
            'flight': '',
        }
        
        for th in time_table.xpath('//thead//tr[1]//th'):
            key = th.text.strip().lower()
            dict_time[key] = ''
            if key in ['departs', 'arrives', 'remarks']:
                dict_time[key] = {}

        for th in time_table.xpath('//thead//tr[2]//th[position() < 5 and position() > 1]'):
            key = th.text.strip().lower()
            dict_time['departs'][key] = ''

        for th in time_table.xpath('//thead//tr[2]//th[position() >= 5]'):
            key = th.text.strip().lower()
            dict_time['arrives'][key] = ''

        flg_has_exit = False
        if not dict_time['arrives'].get('exit') is None:
            flg_has_exit = True

        idx = 1
        td_flight = time_table.xpath('//tbody//tr//td[{idx}]'.format(idx=idx))[0]
        flight = td_flight.text.strip()
        flight = re.sub(r'(\s|(\u3000))+', ' ', flight)
        dict_time['flight'] = flight

        idx += 2

        depart_keys = ['scheduled', 'status', 'gate']
        for i, td in enumerate(time_table.xpath('//tbody//tr//td[position() >= {} and position() < {}]'.format(idx, idx + 3))):
            data = td.text.strip()
            data = re.sub(r'(\s|(\u3000))+', ' ', data)
            if len(td.xpath('span[@class="emData2"]')):
                tmp = ' '.join([node.text.strip() for node in td.xpath('span[@class="emData2"]') if node.text.strip() != ''])
                data += (' {}'.format(tmp))
            dict_time['departs'][depart_keys[i]] = data
            idx += 1

        arrive_end = idx + 2
        arrives_keys = depart_keys[:-1]
        if flg_has_exit:
            arrive_end += 1
            arrives_keys.append('exit')

        for i, td in enumerate(time_table.xpath('//tbody//tr//td[position() >= {} and position() < {}]'.format(idx, arrive_end))):
            data = td.text.strip()
            data = re.sub(r'(\s|(\u3000))+', ' ', data)
            if len(td.xpath('span[@class="emData2"]')):
                tmp = ' '.join([node.text.strip() for node in td.xpath('span[@class="emData2"]') if node.text.strip() != ''])
                data += (' {}'.format(tmp))
            dict_time['arrives'][arrives_keys[i]] = data

        idx = arrive_end
        remarks_keys = ['status', 'note']

        for i, td in enumerate(time_table.xpath('//tbody//tr//td[position() >= {}]'.format(idx))):
            data = td.text.strip()
            data = re.sub(r'(\s|(\u3000))+', ' ', data)
            if len(td.xpath('span')):
                tmp = ' '.join([node.text.strip() for node in td.xpath('span') if isinstance(node.text, str) and node.text.strip() != ''])
                data += (' {}'.format(tmp))
            dict_time['remarks'][remarks_keys[i]] = data.strip()

        return dict_time

class SectionMiles(object):
    def __init__(self, xml_str):
        self.xml_str = xml_str

    def parse_section_miles(self, xml_str=None, encoding='utf-8'):
        if not xml_str:
            xml_str = self.xml_str

        if isinstance(xml_str, str):
            xml_str = xml_str.decode(encoding)

        parsed = etree.XML(xml_str)