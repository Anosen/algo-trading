from src.dataset import TsData

def generate_pickle(csv_dirs, save_path):
    # Load the data
    crypto_data = TsData(csv_dirs=csv_dirs)
    
    # Print the data
    crypto_data.print_data()
    
    # Plot the data
    crypto_data.plot_data()

    # Save the data as a pickle file
    crypto_data.save_pickle(save_path)
    
    # Verify the pickle file can be loaded
    TsData(data_pickle=save_path)

if __name__ == '__main__':
    # Define the paths to the original csv files
    csv_dirs=('/root/dev/Crypto/data/cryptoarchive', 
              '/root/dev/Crypto/data/kraken', 
              '/root/dev/Crypto/data/kaggle'
              )
    
    # Define the path to save the pickle file
    save_path='/root/dev/Crypto/data/dataset.pkl'
    
    # Generate the pickle file
    generate_pickle(csv_dirs, save_path)