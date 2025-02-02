from src.dataset import TsData

def generate_pickle(csv_dir_list, save_path):
    # Load the data
    crypto_data = TsData(csv_dir_list=csv_dir_list, sampling=60*24)
    
    # Print the data
    crypto_data.print_data()
    
    # Plot the data
    crypto_data.plot_data()

    # Save the data as a pickle file
    crypto_data.save_pickle(save_path)
    
    # Verify the pickle file can be loaded
    TsData(pickle_file=save_path)

if __name__ == '__main__':
    # Define the paths to the original csv files
    csv_dir_list=['/root/data/crypto/sources/cryptoarchive',
              '/root/data/crypto/sources/kraken', 
              '/root/data/crypto/sources/kaggle'
              ]
    
    # Define the path to save the pickle file
    save_path='/root/data/crypto/BTCj-2017001-2024096.pkl'
    
    # Generate the pickle file
    generate_pickle(csv_dir_list, save_path)