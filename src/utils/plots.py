from matplotlib import pyplot as plt
import pandas as pd
from src.portfolio import Portfolio
from src.utils.utils import unix2dt


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
