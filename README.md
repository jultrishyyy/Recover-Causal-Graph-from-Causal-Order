# Causal Graph Recovery from Causal Order

This repository provides Python scripts to recover and visualize causal graphs. This is specifically tailored for the VAR-LiNGAM method, which requires a known causal order as input. Other methods might be unable to adapt these scripts. Additionally, the repository contains scripts to generate a ground truth causal order from a summary matrix and to evaluate the accuracy of the recovered graphs.

-----

## 🚀 Getting Started


### Python Version

The scripts were tested using the following version of Python.

```
Python 3.12.9
```

You can check your own Python version by running this command in your terminal:

```bash
python --version
```

### 1\. Installation

To get started, clone the repository and install the necessary Python packages using the `requirements.txt` file.

```bash
git clone https://github.com/jultrishyyy/Recover-Causal-Graph-from-Causal-Order.git
cd Recover-Causal-Graph-from-Causal-Order
pip install -r requirements.txt
```

### 2\. Preparing Your Data

Before running the analysis, ensure your data is correctly formatted and placed in the appropriate directory.

  * **Causal Order**: The causal order of variables should be stored in a `causal_order.txt` file as a Python list.
  * **Ground Truth Summary Matrix**: The ground truth summary matrix must be in a `summary_matrix.npy` file, saved as a NumPy array.
  * **Dataset**: Your dataset should be in a `.csv` file.

All three files for a given dataset must be located in the same subdirectory within the `data/` folder.

**File Structure Example:**

```
root/
└── data/
    └── Dataset1/
        ├── causal_order.txt
        ├── summary_matrix.npy
        └── dataset2.csv
    └── Dataset2/
        ├── causal_order.txt
        ├── summary_matrix.npy
        └── dataset2.csv
    ......
```

**`causal_order.txt` Example:**

```
[0, 1, 2, 3, 5, 4, 6]
```

**`summary_matrix.npy` Example:**

```python
[[0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [1, 1, 1, 1, 0, 1, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [1, 1, 1, 1, 0, 1, 0]]
```

-----

## 📊 Running the Script

To run the script, execute the following command from the root directory:

```bash
python run.py --data_path path/to/your/data --output_path path/to/your/results
```

For example, to process the `Web_Activity` dataset, use its relative path:

```bash
python run.py --data_path data/Web_Activity/ --output_path result/Web_Activity/
```

Alternatively, you can directly modify the paths inside the `run.py` script and run it without arguments for more flexibility:

```bash
python run.py
```

Upon completion, the recovered causal graph and evaluation metrics will be saved in the specified output directory within the `result/` folder.

```
root/
└── data/
    └── Dataset1/
        ├── causal_graph.png
        └── metrics.txt
    └── Dataset2/
        ├── causal_graph.png
        └── metrics.txt
    ......
```

-----

## 📂 Repository Structure

```
root/
├── data/
├── generate_ground_truth/
├── helper/
├── result/
├── run.py
└── requirements.txt
```

### `data/`

This directory contains the datasets. Each dataset has its own subfolder, which includes the raw data and the corresponding ground truth files. The repository includes:

  * **IT Monitoring Data**: `Antivirus_Activity`, `Middleware_oriented_message_Activity`, `Storm_Ingestion_Activity`, and `Web_Activity`. (Source: [Case\_Studies\_of\_Causal\_Discovery](https://github.com/ckassaad/Case_Studies_of_Causal_Discovery_from_IT_Monitoring_Time_Series))
  * **CausalRiver Datasets**: `Flood`. (Source: [CausalRivers](https://github.com/CausalRivers/causalrivers))

### `generate_ground_truth/`

This folder contains scripts for generating synthetic datasets and ground truth summary matrices.

  * `generate_order_from_matrix.py`: Generates a causal order from a given summary matrix.
  * `generate_IT_summary_matrix.py`: Creates summary matrices for the IT monitoring datasets.
  * `generate_causalriver_summary_matrix.py`: Creates summary matrices for the CausalRiver datasets.
  * `process_causalriver.py`: Preprocesses CausalRiver datasets, including handling missing values and resampling.

### `helper/`

This directory contains utility scripts for the causal discovery process.

  * `estimate_adjacency_matrix.py`: Estimates the adjacency matrix based on the provided causal order.
  * `helper_methods.py`: A collection of helper functions, including:
      * `convert_Btaus_to_summary_matrix()`: Converts a `B_taus` matrix to a summary matrix.
      * `plot_summary_causal_graph()`: Constructs and saves a causal graph from a matrix.
      * `prune_summary_matrix_with_best_f1_threshold()`: Prunes the estimated summary matrix using the threshold that yields the best F1 score.
      * `save_results_and_metrics()`: Saves the results and evaluation metrics to the specified path.

### `result/`

This folder stores the output of the analysis. For each dataset, a subfolder is created containing the generated causal graph (`causal_graph.png`) and performance metrics (`metrics.txt`).

-----

## 📝 Notes

  * Ensure that the number of variables in your dataset matches the dimensions of the summary matrix.
  * The `CausalRiverBavaria` and `CausalRiverEastGermany` datasets are too large for this repository. Please download them from the original [CausalRivers GitHub repository](https://github.com/CausalRivers/causalrivers).
  * For large datasets (more than 15 variables), such as `CausalRiverFlood`, visualizing the full causal graph is not recommended as it can become cluttered and difficult to interpret.
  * For any issues or questions, please open an issue on the repository's issue tracker.