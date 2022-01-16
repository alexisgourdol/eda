import pandas as pd
import numpy as np
import seaborn as sns


def count_nan(df: pd.DataFrame, dtype: str = None) -> pd.Series:
    """
    Returns a Series with only the count of NaNs for columns containing NaN values.
    A specific type can be specified to select columns with a specific dtype

    Args:
        df (pd.DataFrame): original pandas DataFrame
        [Optional] dtype (str): selects only a subset of the columns, accepts the same strings as pd.DataFrame.select_dtypes
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html

    Returns:
        pd.Series: count of np.nan, only for columns containing missing values
    """

    if dtype is None:
        return df.isna().sum().pipe(lambda s: s[s > 0]).rename("nan_counts")
    else:
        return (
            df.select_dtypes(include=[dtype])
            .isna()
            .sum()
            .pipe(lambda s: s[s > 0])
            .rename("nan_counts")
        )


def numeric_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with the column names for NUMERIC data types

    Args:
        df (pd.DataFrame): original pandas DataFrame

    Returns:
        pd.Series: with the following MultiIndex :
        - level 0 (MAIN_TYPE): NUMERIC
        - level 1 (detailed_dtype): number, int, int8, int16,
        int32, int64, float, float16, float32, float64, Int64
    """
    # set up the index for the df
    level_1 = np.array(
        [
            "np number",
            "np int",
            "np int8",
            "np int16",
            "np int32",
            "np int64",
            "np float",
            "np float16",
            "np float32",
            "np float64",
            "pd Int64",
        ]
    )
    level_0 = np.full(level_1.shape[0], fill_value="NUMERIC")
    arrays = [level_0, level_1]

    return pd.DataFrame(
        data=[
            [df.select_dtypes(include="number").columns.tolist()],
            [df.select_dtypes(include="int").columns.tolist()],
            [df.select_dtypes(include="int8").columns.tolist()],
            [df.select_dtypes(include="int16").columns.tolist()],
            [df.select_dtypes(include="int32").columns.tolist()],
            [df.select_dtypes(include="int64").columns.tolist()],
            [df.select_dtypes(include="float").columns.tolist()],
            [df.select_dtypes(include="float16").columns.tolist()],
            [df.select_dtypes(include="float32").columns.tolist()],
            [df.select_dtypes(include="float64").columns.tolist()],
            [df.select_dtypes(include="Int64").columns.tolist()],
        ],
        index=arrays,
        columns=["cols"],
    )


def obj_cat_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with the column names for OBJECT and CATEGORICAL data types

    Args:
        df (pd.DataFrame): original pandas DataFrame

    Returns:
        pd.Series: with the following MultiIndex :
        - level 0 (MAIN_TYPE): OBJ / CAT
        - level 1 (detailed_dtype): object, category
    """

    level_1 = np.array(["np object", "pd categorical"])
    level_0 = np.full(level_1.shape[0], fill_value="OBJ / CAT")
    arrays = [level_0, level_1]

    return pd.DataFrame(
        data=[
            [df.select_dtypes(include="object").columns.tolist()],
            [df.select_dtypes(include="category").columns.tolist()],
        ],
        index=arrays,
        columns=["cols"],
    )


def boolean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with the column names for BOOLEAN data types

    Args:
        df (pd.DataFrame): original pandas DataFrame

    Returns:
        pd.Series: with the following MultiIndex :
        - level 0 (MAIN_TYPE): BOOLEAN
        - level 1 (detailed_dtype): bool, boolean
    """
    level_1 = np.array(["np bool", "pd boolean"])
    level_0 = np.full(level_1.shape[0], fill_value="BOOLEAN")
    arrays = [level_0, level_1]

    if pd.__version__ > "1.0.0":

        return pd.DataFrame(
            data=[
                [df.select_dtypes(include="bool").columns.tolist()],
                [df.select_dtypes(include="boolean").columns.tolist()],
            ],
            index=arrays,
            columns=["cols"],
        )
    else:
        print(
            f"""'boolean' datatype is a pandas Nullable boolean type.
            "BooleanArray is currently experimental. Its API or implementation may change without warning.
            "New in version 1.0.0. ; not supported in your pandas version {pd.__version__}"""
        )
        return pd.DataFrame(
            data=[
                [df.select_dtypes(include="bool").columns.tolist()],
                [np.nan],
            ],
            index=arrays,
            columns=["columns"],
        )


def time_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with the column names for TIME data types

    Args:
        df (pd.DataFrame): original pandas DataFrame

    Returns:
        pd.Series: with the following MultiIndex :
        - level 0 (MAIN_TYPE): TIME
        - level 1 (detailed_dtype): datetime, datetimetz, timedelta
    """
    level_1 = np.array(["np datetime", "pd datetimez", "np timedelta"])
    level_0 = np.full(level_1.shape[0], fill_value="TIME")
    arrays = [level_0, level_1]

    return pd.DataFrame(
        data=[
            [df.select_dtypes(include="datetime").columns.tolist()],
            [df.select_dtypes(include="datetimetz").columns.tolist()],
            [df.select_dtypes(include="timedelta").columns.tolist()],
        ],
        index=arrays,
        columns=["cols"],
    )


def all_types_df(df: pd.DataFrame, dropna: bool = None) -> pd.DataFrame:
    """
    Returns a DataFrame that concatenates the MAIN_TYPES :

    Args:
        df (pd.DataFrame): original pandas DataFrame
        [Optional] dropna (bool): removes the data types that do not contain any column name

    Returns:
        pd.DataFrame: with the following MultiIndex :
        - level 0 (MAIN_TYPE): NUMERIC, OBJ / CAT, BOOLEAN, TIME
        - level 1 (detailed_dtype): number, int, int8, int16,
        int32, int64, float, float16, float32, float64, Int64,
        object, category, bool, boolean, datetime, datetimetz, timedelta

    """
    res = pd.concat([numeric_df(df), obj_cat_df(df), boolean_df(df), time_df(df)])
    if dropna is None or dropna == False:
        return res
    if dropna == True:
        # change empty lists (no column name) into np.nan, and remove it
        return res.where(
            res.cols.apply(lambda s: len(s) != 0 if s is not np.nan else np.nan)
        ).dropna()
    else:
        raise ValueError(
            """Invalid value for dropna. Please provide `True`or `False`.
            Defaults to None, which is like `False`"""
        )


def reorder_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function to reorder the columns within `enriched_describe` function

    Args:
        df (pd.DataFrame): resulting DataFrame from `all_types_df` function

    Returns:
        pd.DataFrame: same index, reordered columns
    """
    return df[
        [
            "nan_counts",
            "count",
            "unique",
            "mean",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max",
            "top",
            "freq",
        ]
    ]


def enriched_describe(df: pd.DataFrame, dropna: bool = True) -> pd.DataFrame:
    """
    Returns a DataFrame that
    - segments the columns per data type
    - shows the number of missing values
    - adds the regular result from `pd.DataFrame.describe` function

    Args:
        df (pd.DataFrame): original pandas DataFrame

    Returns:
        pd.DataFrame: with an enhanced view of the describe,
        that wan easily be sliced by data types"""
    return (
        all_types_df(df, dropna=dropna)  # data type segmentation
        .explode("cols")  # turn the list of column names into new rows
        .merge(  # merge with missing values coount
            count_nan(df),
            left_on="cols",
            right_index=True,
            how="left",
        )
        .assign(nan_counts=lambda _df: _df.nan_counts.fillna(0).astype(int))
        .rename_axis(["MAIN_TYPE", "detailed_dtype"])
        .set_index("cols", append=True)  # create a 3-level multi index
        .merge(  # merge with regular describe function
            df.describe(include="all").T.rename_axis("cols"),
            left_index=True,
            right_index=True,
            how="left",
        )
        .pipe(reorder_cols)
        .assign(count=lambda _df: _df.loc[:, "count"].astype(int))
        .fillna("-")
    )


def subset(df: pd.DataFrame, lst: list, level="detailed_dtype"):
    return pd.concat([df.xs(key=t, level=level, drop_level=False) for t in lst], axis=0)


def main():
    pd.set_option("display.max_colwidth", 200)
    pd.set_option("display.float_format", lambda x: "%.2f" % x)
    df = sns.load_dataset("penguins")
    return enriched_describe(df)


if __name__ == "__main__":
    print(main())
