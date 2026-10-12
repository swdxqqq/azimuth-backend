from functools import reduce
from typing import Set, Tuple

import pandas as pd

import load_data as ld

EXCLUDE_COLS = ['Country', 'Year']


def get_intersection_set(dfs: Tuple[pd.DataFrame, ...]) -> Set[str]:
    """Find countries present in all provided DataFrames"""
    sets = [set(df["Country"]) for df in dfs]
    return reduce(lambda left, right: left.intersection(right), sets)


def intersection_all_count() -> None:
    """Print the number of countries present in all years"""
    dfs = ld.results_by_year()
    result = get_intersection_set(dfs)
    print(f"Intersection of all years: {len(result)} rows")


def intersection_all() -> pd.DataFrame:
    """Filter all yearly DataFrames to keep only countries present in every year,
    then concatenate into a single DataFrame"""
    dfs = ld.results_by_year()
    common_countries = get_intersection_set(dfs)
    
    intersected_dfs = [df[df["Country"].isin(common_countries)].copy() for df in dfs]
    
    return pd.concat(intersected_dfs, ignore_index=True)


def validate_data(df: pd.DataFrame) -> None:
    """Print validation info about the DataFrame: structure, stats, nulls, unique countries"""
    print(f"Combined DataFrame Info:\n{df.info()}\n")
    print(f"Description:\n{df.describe()}\n")
    print(f"Null values:\n{df.isnull().sum()}\n")
    print(f"Number of unique countries: {df['Country'].nunique()}")


def normalize_data() -> pd.DataFrame:
    """Apply Min-Max normalization to all numeric columns except Country and Year"""
    df = intersection_all()
    
    numeric_cols = [
        col for col in df.select_dtypes(include=['number']).columns
        if col not in EXCLUDE_COLS
    ]
    
    normalized_df = df.copy()
    col_min = normalized_df[numeric_cols].min()
    col_max = normalized_df[numeric_cols].max()
    normalized_df[numeric_cols] = (normalized_df[numeric_cols] - col_min) / (col_max - col_min)
    
    return normalized_df


def main() -> None:
    df = intersection_all()
    print("Original DataFrame:")
    validate_data(df)
    
    df_normalized = normalize_data()
    print("\nNormalized DataFrame:")
    validate_data(df_normalized)


if __name__ == '__main__':
    main()