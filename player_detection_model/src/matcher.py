from scipy.spatial.distance import cosine, euclidean
from scipy.optimize import linear_sum_assignment
import numpy as np

def match_players(broadcast_feats, tacticam_feats, alpha=0.7):
    if not broadcast_feats or not tacticam_feats:
        return []

    cost_matrix = np.zeros((len(tacticam_feats), len(broadcast_feats)))

    for i, tac in enumerate(tacticam_feats):
        for j, brd in enumerate(broadcast_feats):
            visual = cosine(tac["embedding"], brd["embedding"])
            spatial = euclidean(tac["center"], brd["center"]) / 1000.0
            cost_matrix[i, j] = alpha * visual + (1 - alpha) * spatial

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return list(zip(row_ind, col_ind))  # tacticam_idx -> broadcast_idx
