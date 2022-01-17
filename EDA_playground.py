# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import seaborn as sns
import cookbook_eda as eda

# <codecell>

dir(cookbook_eda)

# <codecell>

file = 'penguins'
df = sns.load_dataset(file); display(df.shape); df.head(3)

# <codecell>

eda.enriched_describe(df)

# <codecell>

def subset(df: pd.DataFrame, lst: list):
    return pd.concat([
        eda_df.xs(key=t, level="detailed_dtype", drop_level=False)
        for t in lst
          ], axis=0)
        

# <codecell>

lst = ["np object", "np float"]
subset(eda_df, lst)

# <codecell>

eda_df = eda.enriched_describe(df)
eda_df

# <codecell>

lst = ["np object", "np float"]
pd.concat([
    eda_df.xs(key=t, level="detailed_dtype", drop_level=False)
    for t in lst
          ], axis=0)

# <codecell>


