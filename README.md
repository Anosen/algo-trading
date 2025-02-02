# 📈 Algorithmic Trading

## Overview
This is a very simple algorithmic trading environment implemented in Python. 

It utilizes historical crypto market data to optimize portfolio performance given a policy and a forecasting model.

The environment supports multiple trading strategy and risk management parameters.

## 🚀 Features
- **Backtesting**: Test your strategy on historical price data.
- **Grid Search**: Find your best parameters by parallelized search.
- **Visualization Tools**: View position opening, closing and returns.
- **Strategy Customization**: Implement and test different trading strategies.
- **Risk Management**: Stop-loss, take-profit, and exposure control.

## 🛠️ Installation
### Requirements
Ensure you have Python installed (>= 3.8). Then, install dependencies:
```bash
pip install -r requirements.txt
```

## 📂 Project Structure
```
algo-trading/
│-- app/                        # Main trading application
│   │-- backtesting/            # Backtesting on historical data
│   │-- grid_search.py          # Grid search multiple parameters
│   │-- analyse_grid_search.py  # Analyse grid search (plot, stats)
│-- data/                       # Historical market data
│-- results/                    # Simulations results
│-- src/                        # Historical market data
│   │-- utils/                  # Utilities
│-- tests/                      # Unit tests
│-- config.py                   # Configuration settings
│-- main.py                     # Entry point for the system
│-- README.md                   # Documentation
```

## 📌 Usage
### Running the System
The system is controlled through `main.py`, which centralizes all execution modes.

#### **Backtesting a Strategy**
Run a backtest with a given strategy:
```bash
python main.py --mode backtest --strategy moving_average \
    --fee 0.001 --init_cash 10000 --init_crypto 0.1 \
    --min_expected_returns 0.02 --stop_loss 0.05 --predict_len 10 \
    --verbose --plot_results
```

#### **Grid Search for Parameter Optimization**
Execute a parameter grid search:
```bash
python main.py --mode grid_search
```

#### **Analyzing Grid Search Results**
Run an analysis on the grid search results:
```bash
python main.py --mode analyse
```

## 🔗 Supported Data Sources
- **Kaggle**
- [**CryptoArchive**](www.cryptoarchive.com.au)
- **[Kraken](www.kraken.com)**

As long as you can format a CSV with column `'unix', 'open', 'high', 'low', 'close', 'volume'`, it'll work.

## 📈 Results & Performance Analysis
The system includes built-in visualization tools to plot:
- Cumulative returns
- Position opening / closing
- Grid search analysis

## 🔧 Configuration
Modify `config.py` to adjust parameters:
```python
config = {
    "data": {
        "pickle_file": "/path/to/pickle",
        "start_position": -1 - 5000,        # Last n time steps
        "end_position": -1,                 # End of data
    },
}
```

## 🔮 Future Enhancements
- Advanced Machine Learning Strategies 🤖
- Multi-Asset Portfolio Optimization 📊
- Mke the fee time variable
- Separate the fixed fee in a maker and taker fee for selling and buying
- Implement take-profit and exposure control
- Switch from Pickle to all CSV

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Contributions are welcome. Please submit a pull request or open an issue for discussion.

## 📧 Contact
For questions, reach out via email or open an issue in the repository.

