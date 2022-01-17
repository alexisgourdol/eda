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

# ## Imports

# <codecell>

import pandas as pd
import numpy as np
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

# <codecell>

with pd.option_context("display.max_colwidth", 200):
    display(eda.all_types_df(df))

# <codecell>

eda_df = eda.enriched_describe(df)
eda_df

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

# <codecell>

lst = ["np object", "np float"]
eda.subset(eda_df, lst)

# <codecell>



# <codecell>

(
    eda_df.assign(histogram_snippet=[f"img/hist_{col}.png"
                                     for col in eda_df.index.get_level_values("cols")])
        .pipe(lambda df: df.to_html(escape=False,
                                    formatters=dict(histogram_snippet=path_to_image_html)
                                   )
             )
)

# <codecell>

def path_to_image_html(path):
    return '<img src="'+ path + '" width="120" >'

# <codecell>

def t():
    return HTML(eda_df.to_html(escape=False, 
           formatters=dict(histogram_snippet=path_to_image_html)
          )
    )

# <codecell>

t()

# <codecell>


