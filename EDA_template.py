# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <markdowncell>

# # Project Name EDA

# <markdowncell>

# ## Project Description

# <markdowncell>

# Goal: 
# 
# Context:
# 
# Data Source:
# 
# Author:

# <markdowncell>

# _______________

# <markdowncell>

# **Data cleaning and exploration notes:**
# 


# <markdowncell>

# - Idea 1
# - Idea 2
# - Idea 3

# <markdowncell>

# ## Imports

# <codecell>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cookbook_eda as eda
from IPython.core.display import HTML

# <markdowncell>

# ## Load data

# <markdowncell>

# [Pandas I/O](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)
# 
# `pd.read_csv`, `pd.read_json`, `pd.read_sql`
# `pd.read_html`,`pd.read_xml`,`pd.read_clipboard`,
# `pd.read_excel`,`pd.read_hdf`,`pd.read_feather`
# `pd.read_parquet`, `pd.read_orc`, `pd.read_sas`, 
# `pd.read_spss`, `pd.read_pickle`, `pd.read_gbq`

# <codecell>

source = 'penguins'
df = sns.load_dataset(source); print(f"shape: {df.shape}, memory: {df.memory_usage(deep=True).sum()}")
df.sample(5)

# <markdowncell>

# ## Explore dtypes

# <codecell>

df.dtypes.rename("data_types").sort_values().to_frame().T

# <codecell>

eda_df = eda.enriched_describe(df)
eda_df

# <codecell>

# remove duplicate outputs
lst = ["np object", "np float"]
eda.subset(eda_df, lst)

# <markdowncell>

# ## Explore distributions

# <codecell>

def hist_num_cols(df):
    num_cols = {col for col in df.select_dtypes(include="number")}

    custom_params = {
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.bottom": True,
        "axes.spines.top": True,
        "axes.grid": False,
    }
    with sns.axes_style("whitegrid", rc=custom_params):

        fig, axs = plt.subplots(nrows=len(num_cols), ncols=1, figsize=(12, 8))

        for idx, col in enumerate(num_cols):
            sns.histplot(x=df[col], data=df, ax=axs[idx], kde=True)
            sns.rugplot(x=df[col], data=df, ax=axs[idx], c="black")
            axs[idx].set_ylabel(col, rotation=0, labelpad=50)
            
hist_num_cols(df)

# <codecell>

def box_num_cols(df):
    num_cols = {col for col in df.select_dtypes(include="number")}

    custom_params = {
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.bottom": True,
        "axes.spines.top": True,
        "axes.grid": False,
    }
    with sns.axes_style("whitegrid", rc=custom_params):

        fig, axs = plt.subplots(nrows=len(num_cols), ncols=1, figsize=(12, 8))

        for idx, col in enumerate(num_cols):
            sns.boxplot(x=df[col], data=df, ax=axs[idx], color="white")
            sns.stripplot(x=df[col], data=df, ax=axs[idx], alpha=0.6)
            axs[idx].set_ylabel(col, rotation=0, labelpad=50)
box_num_cols(df)

# <codecell>

def hist_cat_cols(df):
    num_cols = {col for col in df.select_dtypes(exclude="number")}

    custom_params = {
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.bottom": True,
        "axes.spines.top": True,
        "axes.grid": False,
    }
    with sns.axes_style("whitegrid", rc=custom_params):

        fig, axs = plt.subplots(nrows=len(num_cols), ncols=1, figsize=(12, 8))

        for idx, col in enumerate(num_cols):
            sns.histplot(x=df[col].fillna("NA"), data=df, ax=axs[idx])
            axs[idx].set_ylabel(col, rotation=0, labelpad=50)
            plt.tight_layout()

hist_cat_cols(df)

# <markdowncell>

# Input from Domain Expert:
#   - Missing values
#         - why are some values are missing? 
#         - can they have a meaning? 
#         eg NaN can be replaced by zero, observation should be imputed or discarted etc...
#         
#   - Any apparent issue ? 
#          - e.g. missing unique values in a category
#          - e.g. suspicious distributions, wrong units ...
#   - Candidate columns
#          - object to Categorical
#          - object to bool
#          - float to integer after NaN removal
#          - float precision 
#          - use Nullable type if it makes sense (pd.Int64, pd.Boolean)

# <markdowncell>

# _______________
