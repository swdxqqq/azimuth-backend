from functools import reduce
import numpy as np
import pandas as pd
import load_data as ld


# Находит страны, которые есть во всех датафреймах
def get_intersection_set(dfs):
    sets = [set(df["Country"]) for df in dfs]
    return reduce(lambda left, right: left.intersection(right), sets)


# Количество совпадающих стран
def intersection_all_count():
    dfs = ld.results_by_year()
    result = get_intersection_set(dfs)
    print(f"Intersection of all years: {len(result)} rows")


# Возвращает обрезанные датафреймы только с общими странами     
def intersection_all():
    dfs = ld.results_by_year()
    result = get_intersection_set(dfs)

    intersected_dfs = []
    for df in dfs:
        df_intersection = df[df["Country"].isin(result)].copy()
        intersected_dfs.append(df_intersection)

    result_dfs = {}

    for year, df in zip(range(2014, 2026), intersected_dfs):
        result_dfs[f"res_{year}"] = df
        
    return pd.concat(result_dfs.values(), ignore_index=True)


# Проверка данных
def validate_data(df):
    
    print(f"Combined DataFrame Info:\n{df.info()}\n")
    print(f"Description:\n{df.describe()}\n")
    print(f"Null values:\n{df.isnull().sum()}\n")
    print(f"Number of unique countries: {df['Country'].nunique()}")


# Нормализация min max
def normalize_data():
    df = intersection_all()
    exclude_cols = ['Country', 'Year']
    
    num_cols = [
    col for col in df.select_dtypes(include=['number']).columns 
    if col not in exclude_cols]
    
    min_max_df = df.copy()
    
    min_max_df[num_cols] = (min_max_df[num_cols] - min_max_df[num_cols].min()) / (min_max_df[num_cols].max() - min_max_df[num_cols].min())
    
    return min_max_df

def main():
    df = intersection_all()
    print("Original DataFrame:")
    validate_data(df)
    
    df_normalized = normalize_data()
    print("\nNormalized DataFrame:")
    validate_data(df_normalized)
    
    # intersection_all_count()
    # res_dfs = intersection_all()
    # for df in res_dfs.values():
        # print(len(df))


main()