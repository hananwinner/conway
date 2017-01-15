import unittest
from com.hanan.conway.conway import Conway

class TestNeighbours(unittest.TestCase):
    def test_neighbours(self):
        Conway.neighbours(1, -1, False)
        