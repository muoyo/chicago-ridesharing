"""
##### DATA VISUALIZATIONS #####

This module contains the functions for all the visualizations for our project.

"""

import numpy as np
from scipy import stats


def chi2_contingency(contingency_matrix):
    """This function runs a chi square test for a given contingency matrix."""
    
    return stats.chi2_contingency(np.array(contingency_matrix), False)
