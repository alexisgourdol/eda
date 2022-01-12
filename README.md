# Exploratory Data Analysis

This is a cookbook for my EDA

Auto EDA tools are great to go fast, not so much to really dig into the data and get familiar with it

The helper functions defined here aim to
segment data types.

Some attention has been put in regards to how pandas and numpy handle missing values differently (e.g. `np.nan` turns a dataframe column into a `float`, np.integer cannot have null values, but pandas have a `Int64`nullable data type...)

An enhanced `describe` function encapsulates the early work.

Next steps could include
- comparing the size of dataframes (e.g. before and after preprocessing)
- suggesting visually some manual downcasting (style a df? use the likes of `np.iinfo(np.int16)`and get some boolean to see what could fit, custom styling))
- simple function to snake_case column names, remove spaces, change CamelCase etc...
- for object, check the length distribution , and/or max val (e.g. useful if we want to persist it in a DB to choose proper dtype there)
-some histograms ? use the pctiles for simple boxplots ?
see https://stackoverflow.com/questions/53468558/adding-image-to-pandas-dataframe/53469293
https://towardsdatascience.com/rendering-images-inside-a-pandas-dataframe-3631a4883f60
```python
def check_int_types(df):
    return (
    df.describe(include=[np.int16, np.int32, np.int64])
    .T
    .assign(min_fit_int16 = np.iinfo(np.int16).min < tmp.describe().min())
    .assign(max_fit_int16 = tmp.describe().max()   < np.iinfo(np.int16).max)
    .assign(min_fit_int32 = np.iinfo(np.int32).min < tmp.describe().min())
    .assign(max_fit_int32 = tmp.describe().max()   < np.iinfo(np.int32).max)
    .assign(min_fit_int64 = np.iinfo(np.int64).min < tmp.describe().min())
    .assign(max_fit_int64 = tmp.describe().max()   < np.iinfo(np.int64).max)
)
```
- check cardinality for objects to suggest casting to pd.Category ?

- explore how to expand an simple index with tuples, into a multi index. Some transformation collapsed my multi index, quick googling could not show an efficient way to do "add a level" or expand tuples...

#attempt
"""
    .assign(nan_counts=lambda _df: _df.nan_counts.fillna(0).astype(int))
     #.pipe(lambda _df: _df.pivot_table(values="nan_counts",
     #                                  index=_df.index,
     #                                  columns="columns",
     #                                  aggfunc='max'))
    #.pipe(lambda _df: _df.reindex(_df.index.tolist()))
)


def expand_index(df):
    #split the tuples into new cols
    idx_as_col = df.reset_index()["index"]
    lvl1=idx_as_col.apply(lambda el: el[0])
    lvl2=idx_as_col.apply(lambda el: el[1])
    new_idx = pd.DataFrame([lvl1, lvl2]).T

    #rename and make the indexes match for concatenation
    new_idx.columns=["dt1", "dt2"]
    new_idx= new_idx.set_index(df.index)
    new_df = pd.concat([df, new_idx], axis=1)

    #reindex properly
    return new_df.set_index(["dt1", "dt2"])
expand_index(tmp)
"""
