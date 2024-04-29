
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

def plot_situation(data, portfolio:Portfolio, hold_fig=True):
    # Plot evolution over time
    fig, ax = plt.subplots(2, 1, figsize=(10, 5))
    ax[0].plot(pd.to_datetime(data['unix'], unit='s'), data['close'], color='black', label='Price')
    ax[0].set_title('Price')

    # Plot the trades
    for position in portfolio.position_list:
        if position.entry_date >= data['unix'].iloc[0] and position.entry_date <= data['unix'].iloc[-1]:
            ax[0].axvline(x=unix2dt(position.entry_date), color='green', linestyle='--', ymin=0.0, ymax=0.5)
        if position.closed():
            if position.exit_date >= data['unix'].iloc[0] and position.exit_date <= data['unix'].iloc[-1]:
                ax[0].axvline(x=unix2dt(position.exit_date), color='red', linestyle='--',  ymin=0.5, ymax=1.0)

    # Plot the portfolio value
    ax1 = ax[1]  # First y-axis
    ax1.plot(pd.to_datetime(data['unix'], unit='s'), portfolio.portfolio_value_list, color='tab:blue', label='Portfolio Value')
    ax1.set_ylabel('Value ($)', color='tab:blue')

    # Plot the portfolio returns percentage in the same subplot
    ax2 = ax1.twinx()  # Second y-axis
    portfolio_returns_pct_list = [returns / portfolio.initial_cash for returns in portfolio.portfolio_returns_list]
    ax2.plot(pd.to_datetime(data['unix'], unit='s'), portfolio_returns_pct_list, color='tab:red', label='Portfolio Value')
    ax2.set_ylabel('Value (% of invest)', color='tab:red')
    
    # Set the title of the plot
    ax[1].set_title('Portfolio')
    
    # Adjust subplots
    plt.subplots_adjust(hspace=0.1)
    plt.tight_layout()
    
    fig.legend()
    if hold_fig:
        plt.show()
    else:
        fig.show()