import pandas as pd
from tqdm import tqdm
from src.portfolio import Portfolio
from src.policy import Policy


class Optimizer:
    def __init__(self, portfolio: Portfolio, policy: Policy, predict_len: int, fee=0.03, verbose=False):
        self.portfolio : Portfolio = portfolio
        self.policy = policy
        self.fee = fee
        self.predict_len = predict_len
        self.verbose = verbose

    def iterate_policy(self, data):
        """
        Estimate the returns, given a start portfolio, a policy and a prediction length.
        Applies the policy at each time step of the data.
        Integrates the returns/losses over time.

        Args:
            data (pd.DataFrame): Dataframe with columns 'unix', 'open', 'high', 'low', 'close', 'volume'

        Returns:
            dict: Estimated returns
        """
        if self.verbose:
            print(f'Estimating returns over {len(data)} steps of data')

        for i in tqdm(range(1, len(data))) if self.verbose else range(1, len(data)):
            if self.verbose:
                print(f'Timestep {i} Price: {data.iloc[i]["close"]}')
                print(f'Start: Cash: {self.portfolio.cash} | '
                    f'Crypto: {self.portfolio.crypto} | '
                    f'Portfolio value: {self.portfolio.portfolio_value_list[-1] if len(self.portfolio.portfolio_value_list)>0 else self.portfolio.cash} | '
                    f'Portfolio returns: {self.portfolio.portfolio_returns_list[-1] if len(self.portfolio.portfolio_returns_list)>0 else 0} | '
                    f'Trades: {self.portfolio.trades}')
            
            # Get the past close price
            past_prices = data.iloc[:i]
            
            # Get the predicted close price
            predict_prices = data.iloc[i:i + self.predict_len if i + self.predict_len < len(data) else len(data)]
            
            # # Downsample the predicted prices
            # if len(predict_prices) > 60:
            #     sampled_predict_prices = predict_prices.iloc[::int(len(predict_prices)/60)]
            
            #     if len(sampled_predict_prices) > 0:
            #         predict_prices = sampled_predict_prices

            # Get the past fees
            past_fees = [self.fee for _ in range(len(past_prices))]
            
            # Get the predicted fees
            predict_fees = [self.fee for _ in range(len(predict_prices))]
            
            self.policy.apply_policy(portfolio=self.portfolio,
                                     past_prices=past_prices,
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