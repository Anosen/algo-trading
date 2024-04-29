import pandas as pd


def unix2dt(unix_time):
    """
    Convert a Unix timestamp to a datetime object.
    """
    return pd.to_datetime(unix_time, unit='s')

def cash2qty(cash, entry_price, fee):
    """
    Compute the quantity of the asset that can be bought with the cash.
    """
    # Compute the feed price of the asset
    feed_price = entry_price * (1 + fee)

    # Compute the quantity bought
    quantity = cash / feed_price
    return quantity

def qty2cash(quantity_held, exit_price, exit_fee):
    """
    Compute the cash obtained from selling the asset.
    :param float quantity_held: The quantity of the asset held.
    :param float current_price: The current price of the asset.
    :param float current_fee: The current fee.
    :return float: The cash obtained from selling the asset.
    """
    exit_cash = quantity_held * exit_price * (1 - exit_fee)
    return exit_cash

def compute_returns(entry_cash, quantity_held, exit_price, exit_fee):
    """
    Calculate the returns.
    :param float entry_cash: The cash spent to buy the asset.
    :param float quantity_held: The quantity of the asset held.
    :param float current_price: The current price of the asset.
    :param float current_fee: The current fee.
    :return float: The returns.
    """
    returns = qty2cash(quantity_held, exit_price, exit_fee) - entry_cash
    return returns