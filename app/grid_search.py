import argparse
from pathlib import Path

from src.simulation import estimate_returns
from config import config
import itertools
import pandas as pd
from joblib import Parallel, delayed
from multiprocessing import Queue, Process
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Estimate returns for multiple sets of initial parameters comprised in a search space. Parallelized. Saves the results as a CSV.")

    # Define arguments
    parser.add_argument("--predict_len_list", nargs="+", help="List of: Length of the predicted data (how far in the future we can predict prices)", required=True)
    parser.add_argument("--init_cash_list", nargs="+", help="List of: Initial amount of cash in portfolio", required=True)
    parser.add_argument("--init_crypto_list", nargs="+", help="List of: Initial amount of crypto in portfolio", required=True)

    parser.add_argument("--fee_list", nargs="+", help="List of: The fixed fee for each transaction", required=True)

    parser.add_argument("--min_expected_returns_list", nargs="+", help="List of: The minimum returns that can are expected from a position in order to buy it", required=True)
    parser.add_argument("--stop_loss_list", nargs="+", help="List of: The percentage of loss (compared to the entry price) that triggers the sell of a position (negative float)", required=True)

    parser.add_argument("--verbose", action="store_true", help="Enable short verbose mode")
    parser.add_argument("--plot_results", action="store_true", help="Whether to plot the results of the grid search")

    return parser.parse_args()


def run(*kargs, **kwargs):
    pass


if __name__ == '__main__':
    args = parse_args()

    predict_len_list = [int(predict_len) for predict_len in args.predict_len_list]
    init_cash_list = [float(init_cash) for init_cash in args.init_cash_list]
    init_crypto_list = [float(init_crypto) for init_crypto in args.init_crypto_list]
    fee_list = [float(fee) for fee in args.fee_list]
    min_expected_returns_list = [float(min_expected_returns) for min_expected_returns in args.min_expected_returns_list]
    stop_loss_list = [float(stop_loss) for stop_loss in args.stop_loss_list]
    verbose_list = [False]
    short_verbose_list = [args.verbose]
    plot_results_list = [False]

    print(f'Model prediction capacity: between {min(predict_len_list)} and {max(predict_len_list)} timesteps in the future')
    print(f'Initial cash amount in portfolio: between {min(init_cash_list)}$ and {max(init_cash_list)}$')
    print(f'Initial crypto amount in portfolio: between {min(init_crypto_list)} and {max(init_crypto_list)}')
    print(f'Minimum expected returns to enter a position: between {min(min_expected_returns_list)}$ and {max(min_expected_returns_list)}$')
    print(f'Stop loss: between {min(stop_loss_list)}% and {max(stop_loss_list)}% of the initial cash used to enter a position')
    print(f'Estimating returns...')

    # Generate all parameter combinations
    param_combinations = list(itertools.product(
        predict_len_list, init_cash_list, init_crypto_list, fee_list,
        min_expected_returns_list, stop_loss_list, verbose_list, short_verbose_list, plot_results_list
    ))

    # Define the save path
    results_dir = Path(f'{config["results_dir"]}/{config["data"]["type"]}/grid-search')
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_save_path = results_dir / "grid-search-results.csv"

    # Ensure unique filename if file already exists
    counter = 1
    while csv_save_path.exists():
        csv_save_path = results_dir / f"grid-search-results_{counter}.csv"
        counter += 1

    # Define a queue for parallel writing
    result_queue = Queue()


    # Define a writer function that runs in a separate process
    def csv_writer(queue, save_path):
        """ Continuously writes results from the queue to the CSV file. """
        file_exists = save_path.exists()
        while True:
            result = queue.get()
            if result is None:  # Sentinel value to stop
                break
            df = pd.DataFrame([result])
            df.to_csv(save_path, mode='a', header=not file_exists, index=False)
            file_exists = True  # Ensure header is written only once


    # Start the writer process
    writer_process = Process(target=csv_writer, args=(result_queue, csv_save_path))
    writer_process.start()


    # Define wrapper function
    def run_estimate(params, queue):
        """ Runs the estimation and sends the result to the queue. """
        result = {
            "predict_len": params[0], "init_cash": params[1], "init_crypto": params[2],
            "fee": params[3], "min_expected_returns": params[4], "stop_loss": params[5],
            "verbose": params[6], "short-verbose": params[7], "plot_results": params[8],
            "returns": estimate_returns(*params)
        }
        queue.put(result)  # Send result to writer process
        return result


    # Run in parallel without waiting for writing
    results = Parallel(n_jobs=-1, backend="threading")(
        delayed(run_estimate)(params, result_queue) for params in param_combinations
    )

    # Signal the writer process to stop
    result_queue.put(None)
    writer_process.join()  # Ensure all results are written before exiting

    print(f'Grid search results saved to {csv_save_path}')