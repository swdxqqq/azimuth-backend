import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce

pd.set_option('display.max_columns', None)


# CSV-files loading
def load_data():
    cost_of_living = pd.read_csv('data/cost-of-living_country.csv')
    crime = pd.read_csv('data/crime_country.csv')
    health_care = pd.read_csv('data/health-care_country.csv')
    pollution = pd.read_csv('data/pollution_country.csv')
    property_investment = pd.read_csv('data/property-investment_country.csv')
    traffic = pd.read_csv('data/traffic_country.csv')
    return cost_of_living, crime, health_care, pollution, property_investment, traffic

    # Looking for unique years in every dataset
    # print(cost_of_living['Year'].unique())
    # print(crime['Year'].unique())
    # print(health_care['Year'].unique())
    # print(pollution['Year'].unique())
    # print(property_investment['Year'].unique())
    # print(traffic['Year'].unique())


def map_data():
    cost_of_living, crime, health_care, pollution, property_investment, traffic = load_data()
    names = ['cost', 'crime', 'health', 'pollution', 'property', 'traffic']
    years = [2014, 2015, 2016, 2017, 2018, 2019,
             2020, 2021, 2022, 2023, 2024, 2025]

    dfs_mapping = {
        'cost': cost_of_living,
        'crime': crime,
        'health': health_care,
        'pollution': pollution,
        'property': property_investment,
        'traffic': traffic
    }

    for name in names:
        dfs_mapping[name].drop('Rank', axis=1, inplace=True)

    data_by_years = {}

    for year in years:
        for name in names:
            source_df = dfs_mapping[name]
            variable_name = f"{name}_{year}"
            data_by_years[variable_name] = source_df[source_df['Year'] == year]

    res_data = {}

    for year in years:
        dfs_to_merge = [data_by_years[f'{name}_{year}'] for name in names]
        merged_year_df = reduce(
            lambda left, right: pd.merge(
                left, right, on=['Country', 'Year'], how='inner'
            ),
            dfs_to_merge)
        res_data[f'res_{year}'] = merged_year_df

    return res_data


def print_results_by_year():
    res_data = map_data()
    for year in range(2014, 2026):
        df_year = res_data[f'res_{year}']
        print(f"Year {year}: {len(df_year)} rows")


def results_by_year():
    res_data = map_data()
    df_2014 = res_data['res_2014']
    df_2015 = res_data['res_2015']
    df_2016 = res_data['res_2016']
    df_2017 = res_data['res_2017']
    df_2018 = res_data['res_2018']
    df_2019 = res_data['res_2019']
    df_2020 = res_data['res_2020']
    df_2021 = res_data['res_2021']
    df_2022 = res_data['res_2022']
    df_2023 = res_data['res_2023']
    df_2024 = res_data['res_2024']
    df_2025 = res_data['res_2025']
    return df_2014, df_2015, df_2016, df_2017, df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, df_2024, df_2025

