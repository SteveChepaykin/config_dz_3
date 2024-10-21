from main import parseXmlToConfig, processConfig
import unittest
import os.path as p

class TestMethods(unittest.TestCase):
    def test_make_config(self):
        parseXmlToConfig("test.xml")
        self.assertTrue(p.isfile("test.txt"))
    
    def test_find_packet_2(self):
        processConfig("test.txt")
        self.assertTrue(p.isfile("log.txt"))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)