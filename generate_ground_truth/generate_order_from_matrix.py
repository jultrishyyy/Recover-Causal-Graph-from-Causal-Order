import numpy as np
import os
import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

DATA_PATH = os.path.join(ROOT_DIR, "data", "Storm_Ingestion_Activity")

maxtrix_filename = DATA_PATH + '/summary_matrix.npy'
output_filename = DATA_PATH + '/causal_order.txt'


def find_causal_order_with_levels(adj_matrix):
    """
    Calculates the causal order and its hierarchy (levels) from an adjacency matrix.

    Args:
        adj_matrix (list or np.array): A square matrix where matrix[i][j] = 1
                                      means node j causes node i.

    Returns:
        tuple: A tuple containing:
               - list of lists: The causal order grouped by levels.
               - list: The flattened sorted causal order of acyclic nodes.
               - list: A list of nodes found to be part of a cycle.
    """
    # Convert to numpy array and ignore the diagonal
    matrix = np.array(adj_matrix, dtype=int)
    n_nodes = matrix.shape[0]
    np.fill_diagonal(matrix, 0)

    # Calculate in-degrees for each node
    in_degrees = np.sum(matrix, axis=1)

    # Initialize the queue with all root nodes (in-degree of 0)
    # These are Level 1
    queue = [i for i, degree in enumerate(in_degrees) if degree == 0]
    
    sorted_order = []
    levels = []
    
    # Process nodes level by level
    while queue:
        # All nodes currently in the queue are at the same causal level
        current_level_nodes = sorted(queue)
        levels.append(current_level_nodes)
        
        # Get the number of nodes at the current level to process
        level_size = len(queue)
        
        # Process all nodes at the current level
        for _ in range(level_size):
            u = queue.pop(0)
            sorted_order.append(u)

            # Find effects of u and decrement their in-degrees
            for v in range(n_nodes):
                if matrix[v, u] == 1:
                    in_degrees[v] -= 1
                    # If a node's in-degree becomes 0, it belongs to the next level
                    if in_degrees[v] == 0:
                        queue.append(v)
    
    # Check for cycles
    nodes_in_cycle = []
    if len(sorted_order) < n_nodes:
        all_nodes = set(range(n_nodes))
        sorted_nodes = set(sorted_order)
        nodes_in_cycle = sorted(list(all_nodes - sorted_nodes))

    return levels, sorted_order, nodes_in_cycle



if __name__ == "__main__":

    # Load the adjacency matrix from the file
    matrix = np.load(maxtrix_filename)

    # Find and print the causal order and levels
    causal_levels, causal_order, cyclic_nodes = find_causal_order_with_levels(matrix)


    # Print the results in a structured format
    if not cyclic_nodes:
        print("A unique causal order was found (the graph is a DAG).")
        print("\n--- Causal Order by Level ---")
        for i, level in enumerate(causal_levels):
            print(f"Level {i + 1}: {level}")
        
        print("\n--- Flattened Causal Order List ---")
        print(causal_order)

        # Save the causal order as a list into output_filename
        with open(output_filename, 'w') as f:
            f.write(str(causal_order))
    else:
        print("A unique linear order for all nodes is not possible due to cycles.")
        print("\n--- Causal Order by Level (Acyclic Part) ---")
        for i, level in enumerate(causal_levels):
            print(f"Level {i + 1}: {level}")

        print("\n--- Flattened Causal Order List (Acyclic Part) ---")
        print(causal_order)

        print("\n--- Nodes Found in Cycle(s) ---")
        print(cyclic_nodes)