import argparse
import os
from app import backtesting
from app import grid_search
from app import analyse_grid_search
import config

def parse_args():
    parser = argparse.ArgumentParser(description="Algorithmic Trading Environment")
    parser.add_argument("--mode", choices=["backtest", "grid_search", "analyse"], required=True, help="Mode of operation")
    parser.add_argument("--strategy", type=str, help="Trading strategy to use")
    parser.add_argument("--config", type=str, default="config.py", help="Path to configuration file")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.mode == "backtest":
        if not args.strategy:
            raise ValueError("--strategy is required for backtesting")
        print(f"Running backtest for strategy: {args.strategy}")
        backtesting.run(args.strategy)

    elif args.mode == "grid_search":
        print("Running grid search...")
        grid_search.run()

    elif args.mode == "analyse":
        print("Analyzing grid search results...")
        analyse_grid_search.run()

if __name__ == "__main__":
    main()