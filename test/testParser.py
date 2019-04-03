# encoding: utf-8
import unittest, sys, os

SRC_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(SRC_PATH)

class TestParser(unittest.TestCase):
    def test_DomesticStatus(self):
        from src.lib.parser import DomesticStatus
        with open('test/data/test_default.html', 'r') as f:
            page = f.read()

        parser = DomesticStatus(page)
        time_table = parser.parseTimeTable(parser.getTimeTable())
        print(time_table)

    def test_DomesticStatus_hasError(self):
        from src.lib.parser import DomesticStatus
        with open('test/data/test_error_1.html', 'r') as f:
            page = f.read()

        with self.assertRaises(Exception):
            parser = DomesticStatus(page)

if __name__ == "__main__":
    unittest.main(verbosity=2)