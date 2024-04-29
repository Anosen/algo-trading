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
    
    def __init__(self, cash=1000.0, crypto=0.0):
        """
        Initialize the Portfolio class.
        :param pd.DataFrame data: The data to use for trading.
        :param float cash: The initial cash to trade with.
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

    def buy(self, date, price, cash, fee, schedueled_exit_date=None, schedueled_exit_price=None, schedueled_exit_returns=None, stop_loss=None):
        """
        Buy the all the asset cash can buy.
        :param int date: The date of the transaction.
        :param float price: The price of the asset.
        :param float cash: The cash to spend.
        :param float fee: The fee to pay.
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
            
            # Scheduele the exit
            schedueled_exit_date=schedueled_exit_date,
            schedueled_exit_price=schedueled_exit_price,
            schedueled_exit_returns=schedueled_exit_returns,
            
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
        :return float: The value of the portfolio.
        """
        return self.cash + self.crypto * current_price * (1 - current_fee)
    
    def get_portfolio_returns(self, current_price, current_fee):
        """
        Get the returns of the portfolio.
        :param float current_price: The current price of the asset.
        :return float: The returns of the portfolio.
        """
        return self.get_portfolio_value(current_price, current_fee) - self.initial_cash
    
    def get_portfolio_returns_pct(self, current_price):
        """
        Get the returns percentage of the portfolio.
        :param float current_price: The current price of the asset.
        :return float: The returns percentage of the portfolio.
        """
        return self.get_portfolio_returns(current_price) / self.initial_cash

    def should_buy(self, entry_cash, past_prices, predict_prices, past_fees, predict_fees):
        """
        A method to determine if we should enter a position, based on the predicted prices.
        """
        
        # Get the current close price
        current_price = past_prices.iloc[-1]['close']
        
        # Get the current fee
        current_fee = past_fees[-1]
       
        # Create a list to store the predicted returns
        predicted_returns_list = []

        # Iterate over the future prices
        for i in range(len(predict_prices)):
            # Get the future close price
            future_price = predict_prices.iloc[i]['close']
            
            # Get the future fee
            future_fee = predict_fees[i]
            
            # Compute the potential returns
            quantity_held = cash2qty(entry_cash, current_price, current_fee)
                        
            returns = compute_returns(entry_cash, quantity_held, future_price, future_fee)
            
            predicted_returns_list.append(returns)
            
        # Get the maximum returns
        max_returns = max(predicted_returns_list)
        
        # Get the index of the maximum returns
        max_returns_index = predicted_returns_list.index(max_returns)
        
        # Get the date of the maximum returns
        max_returns_date = predict_prices.iloc[max_returns_index]['unix']
        
        # Get the price of the maximum returns
        max_returns_price = predict_prices.iloc[max_returns_index]['close']
        
        if max_returns > 0:
            return True, max_returns_date, max_returns_price, max_returns
        else:
            return False, None, None, None
    
    def update(self, past_prices, predict_prices, past_fees, predict_fees):
        """
        Apply the policy to update the portfolio.
        """        
        # Get the current date
        current_date = past_prices.iloc[-1]['unix']
        
        # Get the current close price
        current_price = past_prices.iloc[-1]['close']
        
        # Get the current fee
        current_fee = past_fees[-1]
        
        # Determine the cash we can spend
        new_position_cash = self.cash # min(self.cash, max(self.cash * 0.8, 100))
        
        # Determine if we should sell any position
        for position in [pos for pos in self.position_list if pos.active()]:
            sell_bool, new_schedueled_exit_date, new_schedueled_exit_price, new_schedueled_exit_returns = position.should_sell(past_prices, predict_prices, past_fees, predict_fees)
            if sell_bool:
                # Sell
                self.sell(position, current_date, current_price, current_fee)
            else:
                # Update the schedueled exit
                position.update_schedueled_exit(new_schedueled_exit_date, new_schedueled_exit_price, new_schedueled_exit_returns)
        
        # Determine if we should buy a position
        buy_bool, schedueled_exit_date, schedueled_exit_price, schedueled_exit_returns = self.should_buy(new_position_cash, past_prices, predict_prices, past_fees, predict_fees)
        if buy_bool:
            # Buy
            self.buy(
                date=current_date, 
                price=current_price, 
                cash=new_position_cash, 
                fee=current_fee,
                
                # Scheduele the exit
                schedueled_exit_date=schedueled_exit_date, 
                schedueled_exit_price=schedueled_exit_price, 
                schedueled_exit_returns=schedueled_exit_returns,
                
                # Add a stop loss
                stop_loss=-0.05
                )
            
        # Update the portfolio value
        self.portfolio_value_list.append(self.get_portfolio_value(current_price, current_fee))
        
        # Update the portfolio returns
        self.portfolio_returns_list.append(self.get_portfolio_returns(current_price, current_fee))