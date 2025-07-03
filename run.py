import numpy as np
import pandas as pd
from sklearn.utils import check_array
import os
import sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(CURRENT_DIR)
from utils.helper_methods import (
    plot_summary_causal_graph,
    prune_summary_matrix_with_best_f1_threshold,
    save_results_and_metrics,
)
from utils.estimate_adjacency_matrix import estimate_adjacency_matrix
import argparse

parser = argparse.ArgumentParser(description="Estimate and evaluate causal graph.")
parser.add_argument('--data_path', type=str, default=os.path.join(CURRENT_DIR, "data", "Web_Activity"), help='Path to the data directory')
parser.add_argument('--output_path', type=str, default=os.path.join(CURRENT_DIR, "result", "Web_Activity"), help='Path to the output directory')
args = parser.parse_args()

DATA_PATH = args.data_path
OUTPUT_PATH = args.output_path
os.makedirs(OUTPUT_PATH, exist_ok=True)

data_filename = os.path.join(DATA_PATH, 'preprocessed_1.csv')
label_filename = os.path.join(DATA_PATH, 'summary_matrix.npy')
causal_order_filename = os.path.join(DATA_PATH, 'causal_order.txt')
output_metrics_filename = os.path.join(OUTPUT_PATH, 'metrics.txt')
output_graph_filename = os.path.join(OUTPUT_PATH, 'causal_graph.png')



if __name__ == "__main__":

    X = pd.read_csv(data_filename, delimiter=',', index_col=0, header=0)
    X = X.to_numpy()
    X = check_array(X)

    # Load causal order from file
    with open(causal_order_filename, 'r') as f:
        causal_order = f.read().strip()
        causal_order = causal_order.strip('[]')
        causal_order = [int(x) for x in causal_order.split(',')]

    # Estimate adjacency matrix
    estimated_summary_matrix_continuous = estimate_adjacency_matrix(causal_order, X)
    # Load label summary matrix
    label_summary_matrix = np.load(label_filename)
    # Prune estimated summary matrix with best F1 threshold
    estimated_summary_matrix = prune_summary_matrix_with_best_f1_threshold(estimated_summary_matrix_continuous, label_summary_matrix)

    print("\nEstimated summary matrix:")
    print(estimated_summary_matrix)

    # Optional: svae the evaluation results and metrics
    save_results_and_metrics(
        label_summary_matrix,
        estimated_summary_matrix,
        estimated_summary_matrix_continuous,
        order=causal_order,
        filename=output_metrics_filename
    )

    # Plot and save the causal graph
    plot_summary_causal_graph(estimated_summary_matrix, filename=output_graph_filename)

    # Optionally, plot the ground truth causal graph
    # plot_summary_causal_graph(label_summary_matrix, filename=output_graph_filename.replace('.png', '_label.png'))