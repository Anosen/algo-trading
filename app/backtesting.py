import argparse
from src.simulation import estimate_returns


def parse_args():
    parser = argparse.ArgumentParser(description="Estimate returns for a given set of initial parameters.")

    # Define arguments
    parser.add_argument("--predict_len", help="Length of the predicted data (how far in the future we can predict prices)", required=True)

    parser.add_argument("--init_cash", help="Initial amount of cash in portfolio", required=True)
    parser.add_argument("--init_crypto", help="Initial amount of crypto in portfolio", required=True)

    parser.add_argument("--fee", help="The fixed fee for each transaction", required=True)

    parser.add_argument("--min_expected_returns", help="The minimum returns that can are expected from a position in order to buy it", required=True)
    parser.add_argument("--stop_loss", help="The percentage of loss (compared to the entry price) that triggers the sell of a position (negative float)", required=True)

    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("--plot_results", action="store_true", help="Whether to plot the results of the simulation")

    return parser.parse_args()

def run(*kargs, **kwargs):
    pass

if __name__ == '__main__':
    # fee = 0.5
    # init_cash = 5000.0
    # init_crypto = 0.0
    # min_expected_returns = 0.0
    # stop_loss = -2.0
    # predict_len = 50

    args = parse_args()

    fee = float(args.fee)  # TODO: Separate the fee in a MAKER_FEE and a TAKER_FEE for selling and buying
    init_cash = float(args.init_cash)
    init_crypto = float(args.init_crypto)
    min_expected_returns = float(args.min_expected_returns)
    stop_loss = float(args.stop_loss)  # TODO: Also implement a take-profit and exposure control
    predict_len = int(args.predict_len)  # TODO: Add a true forecasting model

    print(f'Model prediction capacity: {predict_len} timesteps in the future')
    print(f'Initial cash amount in portfolio: {init_cash}$')
    print(f'Initial crypto amount in portfolio: {init_crypto}')
    print(f'Minimum expected returns to enter a position: {min_expected_returns}$')
    print(f'Stop loss: {stop_loss}% of the initial cash used to enter a position')
    print(f'Estimating returns...')

    results = estimate_returns(predict_len=predict_len,
                               init_cash=init_cash,
                               init_crypto=init_crypto,
                               fee=fee,
                               min_expected_returns=min_expected_returns,
                               stop_loss=stop_loss,
                               verbose=args.verbose,
                               short_verbose=False,
                               plot_results=args.plot_results)