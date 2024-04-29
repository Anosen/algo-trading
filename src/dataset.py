import os
import pickle
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import cm

class TsData:
    def __init__(self, csv_dirs=None, pickle_file=None):
        """
        Initialize the TsData class.
        :param list csv_dirs: A list of directories containing the CSV files. e.g. ['data/cryptoarchive', 'data/kraken', 'data/kaggle']
        :param str pickle_file: The path to the pickle file containing the data.
        """
        
        self.csv_dirs = csv_dirs
        self.pickle_file = pickle_file
        
        # Get data
        if self.csv_dirs:
            self.data_list = self._load_data(self.csv_dirs)
            self.data = self._combine_data(self.data_list)
        elif pickle_file:
            # Load the crypto dataset
            with open(pickle_file, 'rb') as f:
                self.data = pickle.load(f)
            print(f'Loaded Pickle of shape {self.data.shape}.')

    @staticmethod
    def import_csv(data_folder, cols_to_keep=['unix', 'open', 'high', 'low', 'close', 'volume']):
        # Check if the data folder exists
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f'{data_folder} not found.')
        
        # Get a list of all csv files in the data folder
        csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]
        csv_files.sort()
        
        # Create an empty list to store the dataframes
        dfs = []
        # Iterate over each csv file
        for file in csv_files:
            # Construct the full path of the csv file
            file_path = os.path.join(data_folder, file)
            # Read the csv file into a dataframe
            df = pd.read_csv(file_path)
            # Append the dataframe to the list
            dfs.append(df)
            
        # Concatenate all dataframes into a single dataframe
        data = pd.concat(dfs, ignore_index=True)
        # Sort the dataframe by the 'unix' column
        data = data.sort_values('unix')
        data = data[cols_to_keep]
        data.reset_index(inplace=True)
        
        print(f'Imported {len(data)} entries from {data_folder}')
        return data
    
    def print_data(self, head=3):
        print(f'Fusionned Data:\n{self.data.head(head)}')

    def _load_data(self, csv_dirs):
        data = []
        for csv_dir in csv_dirs:
            data.append(self.import_csv(csv_dir))
        return data
    
    @staticmethod
    def _combine_data(data_list):
        # Combine data
        crypto = pd.concat(data_list, ignore_index=True)
        crypto.drop_duplicates(subset='unix', keep='first', inplace=True)
        crypto = crypto.sort_values('unix', ascending=True)
        crypto.drop(columns='index', inplace=True)
        crypto.reset_index(drop=True, inplace=True)
        print(f'Combined {len(crypto)} entries in total:')
        
        return crypto
    
    def save_pickle(self, path):
        # Save crypto as a pickle file
        with open(path, 'wb') as f:
            pickle.dump(self.data, f)

        print(f'Saved crypto as a numpy pickle file: {path}')
    
    @staticmethod        
    def _get_missing_dates(data):
        # Generate a sequence of all expected dates with one minute intervals
        expected_dates = pd.date_range(start=pd.to_datetime(data['unix'], unit='s').min(), end=pd.to_datetime(data['unix'], unit='s').max(), freq='1min')
        # Find the missing dates by comparing the expected dates with the actual dates in the dataframe
        missing_dates = expected_dates[~expected_dates.isin(pd.to_datetime(data['unix'], unit='s'))]
        
        return missing_dates

    @staticmethod
    def missing_dates_stats(missing_dates, data):
        # Find the closest entries in the crypto date column to one of the missing dates
        displayed_intervals = []
        last_interval = None
        for missing_date in missing_dates:
            if not last_interval or missing_date > last_interval[1]:
                previous_entry = data.loc[data['date'] < missing_date].tail(1)
                next_entry = data.loc[data['date'] > missing_date].head(1)
                closest_entries = pd.concat([previous_entry, next_entry], ignore_index=True)
                interval = (previous_entry['date'].values[0], next_entry['date'].values[0])
                last_interval = interval
                if interval not in displayed_intervals:
                    displayed_intervals.append(interval)
                    print(f"##### {missing_date} #####")
                    print(closest_entries)
        
    def _get_fig(self):
        fig = plt.figure(figsize=(10, 5))
        fig.gca().scatter(pd.to_datetime(self.data['unix'], unit='s'), self.data['open'], s=0.05, color='black', label='Fusionned Sources', marker='x')
        return fig
        
    def plot_data(self):            
        # Plot data
        fig = self._get_fig()
        ax = fig.gca()
        
        # Plot the missing dates
        missing_dates = self._get_missing_dates(self.data)
        ax.scatter(pd.to_datetime(missing_dates, unit='s'), [0 for _ in missing_dates], s=0.05, color='black')
        if self.csv_dirs:
            colors = cm.rainbow(np.linspace(0, 1, len(self.data_list)))
            idx = 0
            for idx, (data, color) in enumerate(zip(self.data_list, colors)):
                current_missing_dates = self._get_missing_dates(data)
                ax.scatter(pd.to_datetime(current_missing_dates, unit='s'), [-500*(idx+1) for _ in current_missing_dates], s=0.05, color=color, label=f'Missing source {idx}')
        
        # Set the x-axis label
        ax.set_xlabel('Date')
        # Set the y-axis label
        ax.set_ylabel('Open')
        # Set the title of the plot
        ax.set_title('Crypto History: Open Prices')
        ax.legend()
        # Rotate the x-axis labels for better readability
        ax.tick_params(axis='x', labelrotation=90)
        # Display the plot
        plt.show()
