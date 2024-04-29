
from matplotlib import pyplot as plt
import pandas as pd
from tqdm import tqdm
from src.portfolio import Portfolio
from src.utils.utils import unix2dt


class Optimizer():
    def __init__(self, portfolio, fee=0.03, verbose=False):
        self.portfolio : Portfolio = portfolio
        self.fee = fee
        self.verbose = verbose
    
    def estimate_returns(self, data, predict_len):
        """
        Iterate over the crypto dataset.
        Look at the close price of the predict_len time steps to decide whether to buy or sell crypto.
        Estimate the cash return of day trading over time.
        """
        print(f'Estimating returns for {len(data)} steps ({len(data)/60} hours or {len(data)/60/24} days) of data')

        for i in tqdm(range(1, len(data))):
            if self.verbose:
                print(f'{i} Price: {data.iloc[i]["close"]}')
                print(f'Start: Cash: {self.portfolio.cash} | '
                    f'Crypto: {self.portfolio.crypto} | '
                    f'Portfolio value: {self.portfolio.portfolio_value_list[-1] if len(self.portfolio.portfolio_value_list)>0 else self.portfolio.cash} | '
                    f'Portfolio returns: {self.portfolio.portfolio_returns_list[-1] if len(self.portfolio.portfolio_returns_list)>0 else 0} | '
                    f'Trades: {self.portfolio.trades}')
            
            # Get the past close price
            past_prices = data.iloc[:i]
            
            # Get the predicted close price
            predict_prices = data.iloc[i:i + predict_len if i + predict_len < len(data) else len(data)]
            
            # Downsample the predicted prices
            if len(predict_prices) > 60:
                sampled_predict_prices = predict_prices.iloc[::int(len(predict_prices)/60)]
            
                if len(sampled_predict_prices) > 0:
                    predict_prices = sampled_predict_prices

            # Get the past fees
            past_fees = [self.fee for _ in range(len(past_prices))]
            
            # Get the predicted fees
            predict_fees = [self.fee for _ in range(len(predict_prices))]
            
            self.portfolio.update(past_prices=past_prices,
                                  predict_prices=predict_prices,
                                  past_fees=past_fees,
                                  predict_fees=predict_fees,
                                  )
            
            if self.verbose:
                print(f'End: Cash: {self.portfolio.cash} | '
                    f'Crypto: {self.portfolio.crypto} | '
                    f'Portfolio value: {self.portfolio.portfolio_value_list[-1]} | '
                    f'Portfolio returns: {self.portfolio.portfolio_returns_list[-1]} | '
                    f'Trades: {self.portfolio.trades}\n')
        
        self.portfolio.sell_all(data.iloc[-1]['unix'], data.iloc[-1]['close'], self.fee)

        return self.portfolio.portfolio_value_list[-1], self.portfolio.portfolio_returns_list[-1], self.portfolio.trades
