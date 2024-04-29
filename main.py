import numpy as np
from config import END_POSITION, PICKLE_DATA, PREDICT_LEN, START_POSITION, UNIX_MONTH
from src.dataset import TsData
from src.optimizer import Optimizer, plot_situation
from src.portfolio import Portfolio


if __name__ == '__main__':
    # Load the data
    data = TsData(pickle_file=PICKLE_DATA).data
    
    # Trim the data
    data = data.iloc[START_POSITION:END_POSITION]

    # Create a portfolio
    portfolio = Portfolio(cash=4000.0, crypto=0.0)
    
    # Create an Optimizer object
    optimize_gains = Optimizer(portfolio, fee=0.005, verbose=False)
    
    # Estimate the returns
    portfolio_value, portfolio_returns, trades = optimize_gains.estimate_returns(data, PREDICT_LEN)
    
    # Print the portfolio value
    print(f'Portfolio value: {portfolio_value}')
    
    # Print the portfolio returns
    print(f'Portfolio returns: {portfolio_returns}')
    
    # Print the portfolio returns percentage
    print(f'Portfolio returns percentage: {portfolio_value/portfolio.initial_cash}')
    
    # Print the trades
    print(f'Trades: {trades}')
    
    plot_situation(data[:-1], portfolio, hold_fig=True)
