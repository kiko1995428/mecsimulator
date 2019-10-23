from simulator.utility.search import search
from simulator.model.device import Device
import unittest


class UtilitySearchTest(unittest.TestCase):
    def setUp(self):
        self.iterable = [Device(name="d1"), Device(name="d2"), Device(name="d3"), Device(name="d4")]

    def test_search_01(self):
        d2 = self.iterable[1]
        dn, index = search(self.iterable, d2)
        self.assertEqual(dn, self.iterable[1])
        self.assertEqual(index, 1)

    def test_search_02(self):
        dn, index = search(self.iterable, "d3", key=lambda d: d.name)
        self.assertEqual(dn, self.iterable[2])
        self.assertEqual(index, 2)
