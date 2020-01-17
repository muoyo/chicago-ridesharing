"""
##### DATA VISUALIZATIONS #####

This module contains the functions for all the visualizations for our project.

"""

import itertools
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# Controls appearance of seaborn plots. Options: paper, notebook, talk, or poster
SEABORN_CONTEXT = 'talk' 
SEABORN_PALETTE = sns.color_palette("dark")



def barplot(x, y, counties, ax, title, color):
    # counties = counties.sort_values(by=y, axis=0, ascending=False)
    
    sns.barplot(counties[x], counties[y], ax=ax, label=y, color=color, alpha=0.6)
    plot_mean_and_ci(counties[y], y, ax, color)
    
    plt.setp(ax.xaxis.get_majorticklabels(),rotation=90)
    ax.yaxis.set_tick_params(labelbottom=True)
    ax.title.set_text(title)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.legend()
    
    return ax



def plot_mean_and_ci(y_series, y, ax, color):    
    ax.axhline(y_series.mean(), color=color, linewidth=5, linestyle='-', label='mean')
    ax.axhspan(y_series.quantile(.05), y_series.quantile(.95), color=color, alpha=0.25, label='95% confidence')

    return ax

    

def barplots_2x2_matrix(dcmi, x, y, figsize=(20, 20), context=SEABORN_CONTEXT,
                        plot_titles=[['Higher Price, Lower % Private Schools', 'Higher Price, Higher % Private Schools'],
                                     ['Lower Price, Lower % Private Schools', 'Lower Price, Higher % Private Schools']]):    

    f, ax = plt.subplots(2, 2, figsize=figsize, sharey=True)

    sns.set_context(context)
    sns.despine(f)    
    
    barplot(x, y, dcmi.high_price_low_pct_private_schools, ax[0][0], plot_titles[0][0], color=SEABORN_PALETTE[7])
    barplot(x, y, dcmi.high_price_high_pct_private_schools, ax[0][1], plot_titles[0][1], color=SEABORN_PALETTE[9])
    barplot(x, y, dcmi.low_price_low_pct_private_schools, ax[1][0], plot_titles[1][0], color=SEABORN_PALETTE[4])
    barplot(x, y, dcmi.low_price_high_pct_private_schools, ax[1][1], plot_titles[1][1], color=SEABORN_PALETTE[7])    

    
    for i in np.arange(0,2):
        for j in np.arange(0,2):
            ax[i][j].set_xlim(-0.5,8-0.5)
        
    plt.tight_layout()
    plt.show()
    
    return f, ax


 
def barplots_side_by_side(dcmi, x, y, plot1_title, plot2_title, figsize=(25,10), context=SEABORN_CONTEXT):
    """
    This function graphs 2 barplots side by side using a DCMetroInfo object

    """
    
    f, ax = plt.subplots(1, 2, figsize=figsize, sharey=True)
    sns.set_context(context)
    sns.despine(f)
        
    barplot(x, y, dcmi.low_price_counties, ax[0], plot1_title, color=SEABORN_PALETTE[4])   
    barplot(x, y, dcmi.high_price_counties, ax[1], plot2_title, color=SEABORN_PALETTE[9])
    
    plt.tight_layout()
    plt.show()

    
    return f, ax

