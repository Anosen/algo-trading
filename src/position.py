from src.utils.utils import cash2qty, qty2cash, compute_returns


class Position:
    """
    A class to represent a trading position.
    :ivar int entry_date: The date the position was bought.
    :ivar float entry_price: The price the asset was bought at.
    :ivar float entry_cash: The cash spent to enter the position.
    :ivar float quantity: The quantity of asset bought.
    :ivar int scheduled_exit_date: The date the position is expected to be sold.
    :ivar float scheduled_exit_price: The price the asset is expected to be sold at.
    :ivar float scheduled_returns: The expected returns at the scheduled exit.
    :ivar float stop_loss: The stop loss percentage.
    :ivar int exit_date: The date the position was sold.
    :ivar float exit_price: The price the asset was sold at.
    :ivar float exit_cash: The cash obtained from selling the asset.
    :ivar float returns: The returns obtained from selling the asset.
    """
    def __init__(self):
        """
        Initialize the Position class.
        """
        super().__init__()
        
        # Effective buying
        self.entry_date = None  # Entry date
        self.entry_price = None  # Entry price
        self.entry_cash = None  # Cash spent to enter the position
        self.quantity = None  # Quantity of asset bought
        
        # Scheduled selling
        self.scheduled_exit_date = None  # Scheduled exit date
        self.scheduled_exit_price = None  # Scheduled exit price
        self.scheduled_returns = None  # Scheduled returns
        
        # Stop loss
        self.stop_loss = None  # Stop loss percentage
        
        # Effective selling
        self.exit_date = None  # Effective exit date
        self.exit_price = None  # Exit price
        self.exit_cash = None  # Exit cash obtained
        self.returns = None  # Cash returns
    
    def active(self):
        """
        Return True if the position was bought but not yet sold, False otherwise.
        """
        if self.entry_date is not None and self.exit_date is None:
            return True
        return False
    
    def closed(self):
        """
        Return True if the position was sold, False otherwise.
        """
        if self.exit_date is not None:
            return True
        return False
    
    def buy(self, date, price, cash, fee, scheduled_exit_date=None, scheduled_exit_price=None, scheduled_exit_returns=None, stop_loss=None):
        """
        Buy the all the asset cash can buy.
        :param int date: The date of the transaction.
        :param float price: The price of the asset.
        :param float cash: The cash to spend.
        :param float fee: The fee to pay.
        :return float: The quantity bought.
        """
        if self.active() or self.closed():
            raise ValueError('The position is already alive.')

        # Save the entry date        
        self.entry_date = date
        
        # Save the entry price
        self.entry_price = price

        # Save the entry cash spent
        self.entry_cash = cash
        
        # Save the scheduled exit
        self.scheduled_exit_date=scheduled_exit_date
        self.scheduled_exit_price=scheduled_exit_price
        self.scheduled_exit_returns=scheduled_exit_returns
        
        # Save the stop loss
        self.stop_loss=stop_loss
        
        # Compute the quantity bought
        self.quantity = cash2qty(cash, self.entry_price, fee)
        
        return self.quantity

    def sell(self, date, price, fee):
        """
        Sell all the asset.
        :param int date: The date of the transaction.
        :param float price: The price of the asset.
        :param float fee: The fee to pay.
        :return float: The returns.
        """
        if not self.active():
            raise ValueError('You need to buy the asset first.')
        
        # Save the exit date
        self.exit_date = date
        
        # Save the exit price
        self.exit_price = price
        
        # Compute the exit cash
        self.exit_cash = qty2cash(self.quantity, self.exit_price, fee)
        
        # Compute the returns
        self.returns = compute_returns(self.entry_cash, self.quantity, self.exit_price, fee)
        
        return self.exit_cash
    
    def should_sell(self, past_prices, predict_prices, past_fees, predict_fees):
        """
        Decide whether to sell the asset.
        :param pd.DataFrame past_prices: The past prices.
        :param pd.DataFrame predict_prices: The predicted prices.
        :param list past_fees: The past fees.
        :param list predict_fees: The predicted fees.
        :return bool: True if the asset should be sold, False otherwise.
        Also returns the optimal date, price and returns to sell the asset in the future if it is better than now.
        """
        # Get the current close price
        current_price = past_prices.iloc[-1]['close']
        
        # Stop loss
        if self.stop_loss is not None:
            
            # Compute the returns if we sold the asset now
            current_returns_pct = compute_returns(self.entry_cash, self.quantity, current_price, past_fees[-1])/self.entry_cash
            
            # Check if the stop loss is reached
            if current_returns_pct < self.stop_loss:
                return True, None, None, None
        
        # Compute the future maximal potential returns
        future_max_returns, max_returns_date, future_max_returns_price, future_max_returns = self._future_returns(predict_prices, predict_fees)
        
        # Compute the immediate potential returns
        immediate_returns = compute_returns(self.entry_cash, self.quantity, current_price, past_fees[-1])      
        
        # Compare the immediate returns with the future returns
        if future_max_returns > immediate_returns and future_max_returns > 0:
            return False, max_returns_date, future_max_returns_price, future_max_returns
        else:
            return True, None, None, None
        
    def _future_returns(self, predict_prices, predict_fees):
        """
        Compute the future returns.
        :param pd.DataFrame predict_prices: The predicted prices.
        :param list predict_fees: The predicted fees.
        :return tuple: The maximum returns, the date of the maximum returns, the price of the maximum returns and the maximum returns.
        """
        predicted_returns_list = []
        
        # Iterate over the future prices
        for i in range(len(predict_prices)):
            # Get the future close price
            future_price = predict_prices.iloc[i]['close']
            
            # Get the future fee
            future_fee = predict_fees[i]
            
            # Compute the returns if we sold the asset at the future price            
            returns = compute_returns(self.entry_cash, self.quantity, future_price, future_fee)
            
            predicted_returns_list.append(returns)
            
        # Get the maximum returns
        future_max_returns = max(predicted_returns_list)
        
        # Get the index of the maximum returns
        future_max_returns_index = predicted_returns_list.index(future_max_returns)
        
        # Get the date of the maximum returns
        max_returns_date = predict_prices.iloc[future_max_returns_index]['unix']
        
        # Get the price of the maximum returns
        future_max_returns_price = predict_prices.iloc[future_max_returns_index]['close']
        
        return future_max_returns, max_returns_date, future_max_returns_price, future_max_returns
        
    
    def update_scheduled_exit(self, new_scheduled_exit_date, new_scheduled_exit_price, new_scheduled_exit_returns):
        """
        Update the scheduled exit.
        """
        self.scheduled_exit_date = new_scheduled_exit_date  # Scheduled exit date
        self.scheduled_exit_price = new_scheduled_exit_price  # Expected price at exit
        self.scheduled_exit_returns = new_scheduled_exit_returns  # Expected returns at exit