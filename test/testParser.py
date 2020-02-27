# encoding: utf-8
import unittest, sys, os

SRC_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(SRC_PATH)

class TestDomesticStatus(unittest.TestCase):
    def setUp(self):
        from src.lib.parser import DomesticStatus
        self.Parser = DomesticStatus

    def test_default(self):
        with open('test/data/test_default.html', 'r') as f:
            page = f.read()

        parser = self.Parser(page)
        time_table = parser.parseTimeTable(parser.getTimeTable())
        self.assertDictEqual(time_table, {
            'flight': 'JAL3537', 
            'departs': {'scheduled': '14:10', 'status': '14:17 Departed', 'gate': '3'}, 
            'arrives': {'scheduled': '15:55', 'status': '16:08 Arrived'}, 
            'remarks': {'status': 'Delayed', 'note': 'due to late arrival of aircraft.'}
        })

    def test_arrive_exit(self):
        with open('test/data/test_arrive_exit.html', 'r') as f:
            page = f.read()
        
        parser = self.Parser(page)
        time_table = parser.parseTimeTable(parser.getTimeTable())
        self.assertDictEqual(time_table, {
            'flight': 'JAL904', 
            'departs': {'scheduled': '11:35', 'status': '11:37 Departed', 'gate': '23'}, 
            'arrives': {'scheduled': '13:45', 'status': '14:04 Arrived', 'exit': 'North Wing'}, 
            'remarks': {'status': '', 'note': ''}
        })

    def test_error_1(self):
        with open('test/data/test_error_1.html', 'r') as f:
            page = f.read()

        with self.assertRaises(Exception):
            parser = self.Parser(page)

class TestSectionMiles(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main(verbosity=2)