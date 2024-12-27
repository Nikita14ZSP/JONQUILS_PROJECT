from typing import List, Dict
import pandas as pd

class DataTransform:
    """
    A class for performing grouping and aggregation on a DataFrame using specified columns and aggregation functions.

    Attributes:
    ----------
    group_columns : List[str]
        A list of column names to group by.
    aggregate_functions : Dict[str, str]
        A dictionary where keys are column names to be aggregated, and values are aggregation functions
        (e.g., 'mean', 'sum').

    Methods:
    -------
    transform(df: pd.DataFrame, used_columns: List[str]=None) -> pd.DataFrame
        Transforms the provided DataFrame by grouping and aggregating based on specified columns and functions.
    """

    def __init__(self, df: pd.DataFrame, group_cols: List[str] = None, aggregate_functions: Dict[str, str] = None):
        """
        Initializes the DataTransform object with specified grouping columns and aggregation functions.

        Parameters:
        ----------
        df : pd.DataFrame
            The DataFrame to be transformed.
        group_cols : List[str], optional
            A list of column names to group by (default is an empty list).
        aggregate_functions : Dict[str, str], optional
            A dictionary of aggregation functions where the key is the column name, and the value is the aggregation
            function (default is an empty dictionary).
        """
        self.df = df
        self.group_columns = group_cols or []
        self.aggregate_functions = aggregate_functions or {}

    def transform(self, used_columns: List[str] = None) -> pd.DataFrame:
        """
        Performs grouping and aggregation based on specified columns and functions.

        Parameters:
        ----------
        used_columns : List[str], optional
            A list of columns to use for grouping and aggregation (default is all columns in the DataFrame `df`).

        Returns:
        ----------
        pd.DataFrame
            A new DataFrame with the results of grouping and aggregation. Column names will be combined
            with the aggregation function used.
        """
        used_columns = used_columns or self.df.columns.tolist()

        # Grouping and aggregating the DataFrame
        grouped_df = self.df[used_columns].groupby(self.group_columns).agg(self.aggregate_functions)

        # Flattening the MultiIndex columns
        grouped_df.columns = [f"{col[0]}_{col[1]}" for col in grouped_df.columns]
        
        return grouped_df.reset_index()  # Reset index to keep group columns in the result

import pandas as pd
import argparse
from DataTransform import DataTransform

def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Data preparation for model training and testing.")
    
    parser.add_argument('--model_test', required=True, type=str, help='Path to data for testing model before deployment')
    parser.add_argument('--raw_data', required=True, type=str, help='Path to raw data')
    parser.add_argument('--not_save_test', action='store_true', help='Flag to skip saving test data')
    parser.add_argument('--not_save_train', action='store_true', help='Flag to skip saving train data')
    parser.add_argument('--not_save_model_test', action='store_true', help='Flag to skip saving model test data')
    parser.add_argument('--out_train', type=str, default='data/features/prepared_train.csv', help='Path to save train data')
    parser.add_argument('--out_test', type=str, default='data/features/prepared_test.csv', help='Path to save test data')
    parser.add_argument('--out_model_test', type=str, default='data/processed/prepared_model_test.csv', help='Path to save model test data')

    return parser.parse_args()

def load_data(path: str) -> pd.DataFrame:
    """Загружает данные из CSV файла."""
    return pd.read_csv(path, parse_dates=True)

def data_filter(df: pd.DataFrame, filter_func) -> pd.DataFrame:
    """Фильтрует DataFrame на основе заданной функции."""
    return df[df.apply(filter_func, axis=1)]

def main() -> None:
    """Основная функция для подготовки данных."""
    args = parse_args()

    # Загрузка данных
    car_train = load_data(args.raw_data + 'car_train.csv')
    model_test = load_data(args.model_test)
    car_test = load_data(args.raw_data + 'car_test.csv')
    fix_info = load_data(args.raw_data + 'fix_info.csv')
    rides_info = load_data(args.raw_data + 'rides_info.csv')

    # Фильтрация данных
    ri_filter_func = lambda row: row['ride_duration'] < 60 * 5 and row['ride_cost'] < 4000 and row['distance'] < 7000
    rides_info = data_filter(rides_info, ri_filter_func)

    GROUPBY_COLUMN = ['car_id']

    # Преобразование fix_info
    fix_info_aggregation = {
        'destroy_degree': ['mean', 'median', 'count'],
        'work_duration': ['sum', 'mean']
    }
    fix_info_transformer = DataTransform(fix_info, group_cols=GROUPBY_COLUMN, aggregate_functions=fix_info_aggregation)

    # Преобразование rides_info
    rides_info_aggregation = {
        'rating': ['mean', 'median'],
        'ride_duration': ['mean', 'median', 'sum'],
        'ride_cost': ['mean', 'median'],
        'speed_avg': ['mean', 'median'],
        'speed_max': ['mean', 'median'],
        'stop_times': ['mean', 'median', 'sum'],
        'distance': ['mean', 'median', 'sum'],
        'refueling': ['sum'],
    }
    rides_info_transformer = DataTransform(rides_info, group_cols=GROUPBY_COLUMN, aggregate_functions=rides_info_aggregation)

    # Применение преобразований
    transformed_fix_info = fix_info_transformer.transform()
    transformed_rides_info = rides_info_transformer.transform()

    # Сохранение результатов
    if not args.not_save_train:
        features = car_train.merge(transformed_fix_info, how='left', on='car_id').merge(transformed_rides_info, how='left', on='car_id')
        features.drop(columns=['car_id'], inplace=True)
        features.to_csv(args.out_train, index=False, encoding='utf-8')

    if not args.not_save_test:
        features_test = car_test.merge(transformed_fix_info, how='left', on='car_id').merge(transformed_rides_info, how='left', on='car_id')
        features_test.drop(columns=['car_id'], inplace=True)
        features_test.to_csv(args.out_test, index=False, encoding='utf-8')

    if not args.not_save_model_test:
        features_model_test = model_test.merge(transformed_fix_info, how='left', on='car_id').merge(transformed_rides_info, how='left', on='car_id')
        features_model_test.drop(columns=['car_id'], inplace=True)
        features_model_test.to_csv(args.out_model_test, index=False, encoding=' utf-8')

if __name__ == '__main__':
    main()
