import unittest
import market_participation


class TestMarket(unittest.TestCase):

    def setUp(self):
        self.market = market_participation.Market(10000)

    def test_market_volume(self):
        self.assertEqual(self.market.volume, 10000)
        

class TestMarketAndParticipant(unittest.TestCase):

    def setUp(self):
        self.market = market_participation.Market(10000)
        self.participant = market_participation.Participant(20000, 0.2, self.market)

    def test_updated_market_volume(self):
        self.assertEqual(self.market.volume, 12500)
        

if __name__ == '__main__':
    unittest.main()
