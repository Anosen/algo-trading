import os

# Get the absolute path to the project root folder
project_root = os.path.dirname(os.path.abspath(__file__))

PICKLE_DATA = f'{project_root}/resources/price_history/BTC/BTCj-2017001-2024096.pkl'  # TODO: Switch from Pickle to all CSV
DATA_TYPE = PICKLE_DATA.split("/")[-1][:4]
RESULTS_DIR = f'{project_root}/results'

UNIX_MONTH = 2629743

# --- Data parameters ---
# Get a window of data start
START_POSITION = -1 -5000  # Last n time steps
# START_POSITION = len(data) - 60*24*7  # Last days
# START_POSITION = np.random.randint(0, len(data) - UNIX_MONTH)  # Random position

# Get the end position
END_POSITION = -1  # End of data
# END_POSITION = START_POSITION + UNIX_MONTH if START_POSITION + UNIX_MONTH < len(data) else len(data)  # One month

# --- Model parameters ---
# Set the maximum prediction duration
MAKER_FEE = 0.4  # Selling fee (https://help.coinbase.com/en/exchange/trading-and-funding/exchange-fees)
TAKER_FEE = 0.6  # Buying fee
