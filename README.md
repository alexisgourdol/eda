# Exploratory Data Analysis

This is a cookbook for my EDA

Auto EDA tools are great to go fast, not so much to really dig into the data and get familiar with it

The helper functions defined here aim to
segment data types.

Some attention has been put in regards to how pandas and numpy handle missing values differently (e.g. `np.nan` turns a dataframe column into a `float`, np.integer cannot have null values, but pandas have a `Int64`nullable data type...)

An enhanced `describe` function encapsulates the early work.

Next steps could include
- comparing the size of dataframes (e.g. before and after preprocessing)
- suggesting visually some manual downcasting (style a df?)
- check cardinality for objects to suggest casting to pd.Category ?
