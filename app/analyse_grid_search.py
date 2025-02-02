import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from config import RESULTS_DIR, DATA_TYPE


def analyse_grid_search(csv_path, save_path=None):
    """ Analyse the grid search results

    Args:
        csv_path (str): Path to the csv file with grid search results
        save_path (str): Path to the folder where the figures will be saved
    """
    # Read the csv
    df = pd.read_csv(csv_path)

    # Define the parameter to optimize
    target_metric = "returns"
    parameters = ["predict_len", "init_cash", "init_crypto", "fee", "min_expected_returns", "stop_loss"]

    # Pairplot to show relationships between parameters
    sns.pairplot(df, vars=parameters,
                 hue=target_metric, palette="coolwarm")
    plt.savefig(f'{save_path}/pair-plot.png')
    plt.close()

    # Correlation heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap of Parameters and Result")
    plt.savefig(f'{save_path}/heatmap.png')
    plt.close()

    # Plot each parameter vs. results
    for param in parameters:
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x=df[param], y=df[target_metric], hue=df[target_metric], palette="coolwarm")
        plt.title(f"{target_metric} vs {param}")
        plt.xlabel(param)
        plt.ylabel(target_metric)
        plt.savefig(f'{save_path}/{param}.png')
        plt.close()

    # Plot the evolution of parameters with the others fixed
    # Iterate over each parameter
    for param in parameters:
        plt.figure(figsize=(10, 6))

        # Get unique values for the parameter being plotted
        unique_values = df[param].unique()

        # Iterate over each unique value of the parameter
        for value in unique_values:
            # Filter dataset where param == value
            subset_df = df[df[param] == value]

            # Sort by another parameter (to see trends)
            varying_param = "init_cash" if param != "init_cash" else "predict_len"
            subset_df = subset_df.sort_values(varying_param)

            # Plot the curve
            plt.plot(subset_df[varying_param], subset_df[target_metric], marker='o', label=f"{param} = {value}")

        # Customize the plot
        plt.xlabel(varying_param)
        plt.ylabel(target_metric)
        plt.title(f"Effect of {param} on {target_metric} (Other Params Fixed)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{save_path}/varying_{param}.png")
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse the grid search and plot the results.")

    parser.add_argument("--csv_path", help="Path to the csv file with grid search results", required=True)
    parser.add_argument("--save_path", help="Path to the folder where the figures will be saved", required=True)

    args = parser.parse_args()

    analyse_grid_search(args.csv_path, args.save_path)