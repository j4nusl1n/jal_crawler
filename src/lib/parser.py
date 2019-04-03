# encoding: utf-8

from lxml import etree
import re

class DomesticStatus(object):

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
        node_list = self.page_tree.xpath('//div[@id="completedTable-body"]//table')
        if len(node_list):
            return node_list[0]
        
        return None

    def parseTimeTable(self, time_table):
        dict_time = {
            'flight': '',
        }
        
        for th in time_table.xpath('//thead//tr[1]//th'):
            key = th.text.strip().lower()
            dict_time[key] = ''
            if key in ['departs', 'arrives']:
                dict_time[key] = {}

        for th in time_table.xpath('//thead//tr[2]//th[position() < 5 and position() > 1]'):
            key = th.text.strip().lower()
            dict_time['departs'][key] = ''

        for th in time_table.xpath('//thead//tr[2]//th[position() >= 5]'):
            key = th.text.strip().lower()
            dict_time['arrives'][key] = ''

        key_list = [
            'flight',
            'departs:scheduled',
            'departs:status',
            'departs:gate',
            'arrives:scheduled',
            'arrives:status'
        ]
        i = 0
        for td in time_table.xpath('//tbody//tr//td'):
            # etree.dump(td)
            # print(td.xpath('span[@class="emData2"]'))
            data = td.text.strip()
            data = re.sub(r'(\s|(\u3000))+', ' ', data)
            if data != '':
                keys = key_list[i].split(':')
                if len(keys) == 1:
                    dict_time[keys[0]] = data
                else:
                    if len(td.xpath('span[@class="emData2"]')):
                        tmp = ' '.join([node.text.strip() for node in td.xpath('span[@class="emData2"]') if node.text.strip() != ''])
                        data += (' {}'.format(tmp))
                    dict_time[keys[0]][keys[1]] = data
                i += 1

        return dict_time