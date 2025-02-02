from src.utils.utils import cash2qty, compute_returns
from src.portfolio import Portfolio

class Policy:
    def __init__(self, min_expected_returns, stop_loss=-2.0):
        """
        Initialize the Policy class.
        :param float min_expected_returns: Threshold stating the minimum expected returns required to buy a position.
        :param float stop_loss: The minimum loss percentage that triggers a sell (a good value is: abs(stop_loss) > 2*fee).
        """
        super().__init__()

        self.min_expected_returns = min_expected_returns
        self.stop_loss = stop_loss


    def __should_buy(self, entry_cash, past_prices, predict_prices, past_fees, predict_fees):
        """
        Private method to determine if we should enter a position, based on the predicted prices.
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

        if max_returns > self.min_expected_returns:
            return True, max_returns_date, max_returns_price, max_returns
        else:
            return False, None, None, None


    def apply_policy(self, portfolio, past_prices, predict_prices, past_fees, predict_fees):
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
        new_position_cash = min(portfolio.cash, max(portfolio.cash * 0.1, 300))  # portfolio.cash

        # Determine if we should sell any position
        for position in [pos for pos in portfolio.position_list if pos.active()]:
            sell_bool, new_scheduled_exit_date, new_scheduled_exit_price, new_scheduled_exit_returns = position.should_sell(
                past_prices, predict_prices, past_fees, predict_fees)
            if sell_bool:
                # Sell
                portfolio.sell(position, current_date, current_price, current_fee)
            else:
                # Update the scheduled exit
                position.update_scheduled_exit(new_scheduled_exit_date, new_scheduled_exit_price,
                                                new_scheduled_exit_returns)

        # Determine if we should buy a position
        buy_bool, scheduled_exit_date, scheduled_exit_price, scheduled_exit_returns = self.__should_buy(
            new_position_cash, past_prices, predict_prices, past_fees, predict_fees)
        if buy_bool:
            # Buy
            portfolio.buy(
                date=current_date,
                price=current_price,
                cash=new_position_cash,
                fee=current_fee,

                # Schedule the exit
                scheduled_exit_date=scheduled_exit_date,
                scheduled_exit_price=scheduled_exit_price,
                scheduled_exit_returns=scheduled_exit_returns,

                # Add a stop loss
                stop_loss=self.stop_loss
            )

        # Update the portfolio value
        portfolio.portfolio_value_list.append(portfolio.get_portfolio_value(current_price, current_fee))

        # Update the portfolio returns
        portfolio.portfolio_returns_list.append(portfolio.get_portfolio_returns(current_price, current_fee))