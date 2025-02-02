import os

from config import PICKLE_DATA, START_POSITION, END_POSITION, RESULTS_DIR, DATA_TYPE
from src.dataset import TsData
from src.optimizer import Optimizer
from src.policy import Policy
from src.portfolio import Portfolio
from src.utils.plots import plot_situation


def estimate_returns(predict_len, init_cash, init_crypto, fee, min_expected_returns, stop_loss, verbose=False, short_verbose=False, plot_results=False):
    """ Computes the returns for a given prediction length.

    Args:
        predict_len (int): the length of the predicted data.
        init_cash (float): the initial amount of cash
        init_crypto (float): the initial amount of crypto
        fee (float): the fee at each transaction
        min_expected_returns (float): the minimum expected returns in the future to buy a position
        stop_loss (float): the loss percentage that triggers the sell of a position (compared to the entry price)
        verbose (bool): whether to print results in the console
        short_verbose (bool): whether to print the short version of the results in the console (for grid search)
        plot_results (bool): whether to plot results and save in the results folder
    """
    # Load data
    data = TsData(pickle_file=PICKLE_DATA).data

    # Trim data
    data = data.iloc[START_POSITION:END_POSITION]

    # Create a portfolio
    portfolio = Portfolio(cash=init_cash, crypto=init_crypto)

    # Create a policy
    policy = Policy(min_expected_returns=min_expected_returns, stop_loss=stop_loss)

    # Create an optimizer
    optimizer = Optimizer(portfolio=portfolio, policy=policy, predict_len=predict_len, fee=fee, verbose=False)

    # Estimate the returns by iterating the policy over time
    optimizer.iterate_policy(data)

    # Get the final returns
    final_portfolio_value = portfolio.portfolio_value_list[-1]
    final_portfolio_returns = portfolio.portfolio_returns_list[-1]
    num_trades = portfolio.trades

    if verbose:
        # Print the portfolio value
        print(f'Portfolio final value: {final_portfolio_value:.2f}$ (initially {init_cash:.2f}$)')

        # Print the portfolio returns
        print(f'Portfolio returns: {final_portfolio_returns:.2f}$')

        # Print the portfolio returns percentage
        print(f'Portfolio returns percentage: {100 * final_portfolio_value / portfolio.initial_cash:.2f}%')

        # Print the trades
        print(f'Trades: {num_trades}')

    if plot_results:
        # Plot the portfolio evolution
        save_path = f'{RESULTS_DIR}/{DATA_TYPE}/fee{fee}/pred{predict_len}/portfolio-returns.png'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Create the folder
        plot_situation(data[:-1], portfolio, predict_len=predict_len, hold_fig=True, save_path=save_path)

    if short_verbose:
        print(f'{predict_len}, {init_cash}, {init_crypto}, {fee}, {min_expected_returns}, {stop_loss}'
              f' Returns {final_portfolio_returns:.2f}')

    return final_portfolio_returns
