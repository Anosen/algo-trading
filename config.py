import os

# Get the absolute path to the project root folder
project_root = os.path.dirname(os.path.abspath(__file__))

UNIX_MONTH = 2629743  # Duration of a month in UNIX

config = {
    "data": {
        "pickle_file": f'{project_root}/data/price_history/BTC/BTCj-2017001-2024096.pkl',  # TODO: Switch from Pickle to all CSV
        
        "start_position": -1 - 5000,  # Last n time steps
        # "start_position": len(data) - 60*24*7   # Last days
        # "start_position": np.random.randint(0, len(data) - UNIX_MONTH)  # Random position

        "end_position": -1,  # End of data
        # "end_position": START_POSITION + UNIX_MONTH if START_POSITION + UNIX_MONTH < len(data) else len(data)  # One month
    },

    "results_dir": f'{project_root}/results',
}

# Get data type
config['data']['type'] = config['data']['pickle_file'].split("/")[-1][:4]

# --- Model parameters ---
# Set the maximum prediction duration
# MAKER_FEE = 0.4  # Selling fee (https://help.coinbase.com/en/exchange/trading-and-funding/exchange-fees)
# TAKER_FEE = 0.6  # Buying fee
