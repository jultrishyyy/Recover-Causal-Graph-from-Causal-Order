import numpy as np
from sklearn.linear_model import LassoLarsIC, LinearRegression
from sklearn.preprocessing import StandardScaler

def predict_adaptive_lasso(X, predictors, target, gamma=1.0):
    """Predict with Adaptive Lasso.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Training data, where n_samples is the number of samples
        and n_features is the number of features.
    predictors : array-like, shape (n_predictors)
        Indices of predictor variable.
    target : int
        Index of target variable.

    Returns
    -------
    coef : array-like, shape (n_features)
        Coefficients of predictor variable.
    """
    # Standardize X
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # Pruning with Adaptive Lasso
    lr = LinearRegression()
    lr.fit(X_std[:, predictors], X_std[:, target])
    weight = np.power(np.abs(lr.coef_), gamma)
    reg = LassoLarsIC(criterion="bic")
    reg.fit(X_std[:, predictors] * weight, X_std[:, target])
    pruned_idx = np.abs(reg.coef_ * weight) > 0.0

    # Calculate coefficients of the original scale
    coef = np.zeros(reg.coef_.shape)
    if pruned_idx.sum() > 0:
        lr = LinearRegression()
        pred = np.array(predictors)
        lr.fit(X[:, pred[pruned_idx]], X[:, target])
        coef[pruned_idx] = lr.coef_

    return coef

def estimate_adjacency_matrix(causal_order, X, prior_knowledge=None):
    """Estimate adjacency matrix by causal order.

    Parameters
    ----------
    causal_order : List-like, shape (n_variables,)
    X : array-like, shape (n_samples, n_features)
        Training data, where n_samples is the number of samples
        and n_features is the number of features.
    prior_knowledge : array-like, shape (n_variables, n_variables), optional (default=None)
        Prior knowledge matrix.

    Returns
    -------
    adjacency_matrix : array-like, shape (n_features, n_features)
        Returns the estimated adjacency matrix, where n_features is the number of features.
    """
    if prior_knowledge is not None:
        pk = prior_knowledge.copy()
        np.fill_diagonal(pk, 0)

    adjacency_matrix = np.zeros([X.shape[1], X.shape[1]], dtype="float64")
    for i in range(1, len(causal_order)):
        target = causal_order[i]
        predictors = causal_order[:i]

        # Exclude variables specified in no_path with prior knowledge
        if prior_knowledge is not None:
            predictors = [p for p in predictors if pk[target, p] != 0]

        # target is exogenous variables if predictors are empty
        if len(predictors) == 0:
            continue

        adjacency_matrix[target, predictors] = predict_adaptive_lasso(X, predictors, target)

    return np.abs(adjacency_matrix)