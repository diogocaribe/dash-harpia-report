import unittest
from app.data import PerformanceReport, DataTradeFromProfitCsv

a = PerformanceReport(trader_name='Diogo Caribé de Sousa', df = DataTradeFromProfitCsv('test/data/20220824_relatorio_performace.csv').df)

class TestPerformanceReport(unittest.TestCase):
    
    def test_trader_name(self):
        """Test o trader name
        # Diogo Caribé de Sousa -> Diogo Caribé de Sousa
        """
        self.assertEqual(a.trader_name, 'Diogo Caribé de Sousa')
    
    def test_trader_saldo(self):
        """Profits from trades.
        """        
        self.assertEqual(a.saldo(), -3598.46)
    
    def test_num_trade(self):
        """Count number of trader
        """        
        self.assertEqual(a.num_trade(), 880)
    
    def test_num_trade_win(self):
        """Count number of win trades
        """        
        self.assertEqual(a.num_trade_win(), 136)
    
    def test_num_trade_loss(self):
        """Count number of losses trades
        """        
        self.assertEqual(a.num_trade_loss(), 672)

    def test_num_trade_zero(self):
        """Count number of trades that neither lose nor win
        """        
        self.assertEqual(a.num_trade_zero(), 72)

    def test_trader_win_percent(self):
        """_win_
        """        
        self.assertAlmostEqual(a.perc_trade_win(), 15.45)

    def test_mean_trade_win(self):
        """Mean trade win
        """        
        self.assertEqual(a.mean_trade_win(), 81.87)
    
    def test_mean_trade_loss(self):
        """Mean trade loss
        """        
        self.assertEqual(a.mean_trade_loss(), -21.92)

    def test_ratio_mean_trade_win_loss(self):

        """_summary_
        """
        self.assertEqual(a.ratio_mean_trade_win_loss(), 3.73)

    def test_ctf(self):
        """_summary_
        """        
        ctf = 1.545 + 3.73 
        self.assertEqual(a.ctf(), ctf)

if __name__ == '__name__':
    unittest.main()
