from typing import List
from src.position import Position
from src.utils.utils import cash2qty, compute_returns


class Portfolio:
    """
    A class to represent a trading portfolio of positions.
    :ivar float cash: The cash currently available.
    :ivar float initial_cash: The initial cash deposited.
    :ivar List[float] cash_list: The list of cash values over time.
    :ivar float crypto: The crypto currently held.
    :ivar List[float] crypto_list: The list of crypto values over time.
    :ivar List[Position] position_list: The list of positions held.
    :ivar int trades: The number of trades.
    :ivar List[float] portfolio_value_list: The list of portfolio values over time.
    :ivar List[float] portfolio_returns_list: The list of portfolio returns over time.
    """
    
    def __init__(self, cash, crypto):
        """
        Initialize the Portfolio class.
        :param float cash: The initial cash amount.
        :param float crypto: The initial crypto amount.
        """
        super().__init__()
        
        self.cash = cash  # Cash currently available
        self.initial_cash = cash  # Initial cash deposited
        self.cash_list = [cash]  # List of cash values over time
        
        self.crypto = crypto  # Crypto currently held
        self.crypto_list = [crypto]  # List of crypto values over time
        
        self.position_list : List[Position] = []  # List of positions held
        
        self.trades = 0  # Number of trades
        
        self.portfolio_value_list = []  # List of portfolio values over time
        
        self.portfolio_returns_list = []  # List of portfolio returns over time

        
    def sell(self, position:Position, date, price, fee):
        self.crypto -= position.quantity
        self.crypto_list.append(self.crypto)
        self.cash += position.sell(date, price, fee)
        self.cash_list.append(self.cash)
        self.trades += 1

    def buy(self, date, price, cash, fee, scheduled_exit_date=None, scheduled_exit_price=None, scheduled_exit_returns=None, stop_loss=None):
        """
        Buy the all the asset cash can buy.
        :param int date: The date of the transaction.
        :param float price: The price of the asset.
        :param float cash: The cash to spend.
        :param float fee: The fee to pay.
        :param int scheduled_exit_date: The date of scheduled exit.
        :param int scheduled_exit_price: The price at scheduled exit date.
        :param int scheduled_exit_returns: The returns at scheduled exit date.
        :param int stop_loss: The defined stop loss, as a negative percent of cash invested to buy the asset.
        :return float: The quantity bought.
        """
        # Verify that the cash is not greater than the available cash
        if cash > self.cash:
            raise ValueError('Not enough cash to buy the asset.')
        
        quantity = cash2qty(cash, price, fee)
        
        # Update the cash
        self.cash -= cash
        self.cash_list.append(self.cash)
        
        # Create a new position
        position = Position()
        
        # Buy the crypto
        self.crypto += position.buy(
            date=date, 
            price=price, 
            cash=cash, 
            fee=fee,
            
            # Schedule the exit
            scheduled_exit_date=scheduled_exit_date,
            scheduled_exit_price=scheduled_exit_price,
            scheduled_exit_returns=scheduled_exit_returns,
            
            # Add a stop loss
            stop_loss=stop_loss,
            )
        self.crypto_list.append(self.crypto)
        
        # Add the position to the list
        self.position_list.append(position)
        
        # Update the number of trades
        self.trades += 1
        
        return quantity
    
    def sell_all(self, date, price, fee):
        """
        Sell all the crypto.
        :param int date: The date of the transaction.
        :param float price: The price of the asset.
        :param float fee: The fee to pay.
        :return float: The cash obtained from selling the asset.
        """
        cash = self.crypto * price * (1 - fee)
        
        # Update the cash
        self.cash += cash
        self.cash_list.append(self.cash)
        # Update the crypto
        self.crypto = 0.0
        
        # Close all positions
        for position in [position for position in self.position_list if position.active()]:
            position.sell(date, price, fee)
        
        return cash
    
    def get_portfolio_value(self, current_price, current_fee):
        """
        Get the value of the portfolio.
        :param float current_price: The current price of the asset.
        :param float current_fee: The current transaction fee
        :return float: The value of the portfolio.
        """
        return self.cash + self.crypto * current_price * (1 - current_fee)
    
    def get_portfolio_returns(self, current_price, current_fee):
        """
        Get the returns of the portfolio compared to the initial invested cash.
        :param float current_price: The current price of the asset.
        :param float current_fee: The current transaction fee
        :return float: The returns of the portfolio.
        """
        return self.get_portfolio_value(current_price, current_fee) - self.initial_cash

    def get_portfolio_returns_pct(self, current_price, current_fee):
        """
        Get the returns percentage of the portfolio compared to the initial invested cash.
        :param float current_price: The current price of the asset.
        :param float current_fee: The current transaction fee
        :return float: The returns percentage of the portfolio.
        """
        return self.get_portfolio_returns(current_price, current_fee) / self.initial_cash