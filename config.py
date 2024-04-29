UNIX_MONTH = 2629743
PICKLE_DATA = '/root/data/crypto/dataset.pkl'

# Get a window of data start
START_POSITION = -1 - 1000  # Last steps
# START_POSITION = len(data) - 60*24*7  # Last days
# START_POSITION = np.random.randint(0, len(data) - UNIX_MONTH)  # Random position

# Get the end position
END_POSITION = -1  # End of data
# end_position = START_POSITION + UNIX_MONTH if START_POSITION + UNIX_MONTH < len(data) else len(data)  # One month

# Set the maximum prediction duration
PREDICT_LEN = 60*3