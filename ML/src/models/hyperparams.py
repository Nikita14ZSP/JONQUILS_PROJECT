import argparse
import json
import logging
from typing import Tuple, Dict, Any
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import (accuracy_score, roc_auc_score, 
                             f1_score, recall_score)
from sklearn.model_selection import train_test_split, GridSearchCV

def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Hyperparameters selection")
    parser.add_argument("-d", "--data_path", required=True, help="PATH to prepared data")
    parser.add_argument("-o", "--output_path", required=True, help="Output path for model_params")
    parser.add_argument("-m", "--metrics", required=True, help="Metrics to use")
    return parser.parse_args()

def load_train_data(data_path: str) -> pd.DataFrame:
    """Загрузка и предобработка данных."""
    logging.info("Loading training data from %s", data_path)
    data = pd.read_csv(data_path)
    data.drop(columns=['target_reg'], inplace=True)
    logging.info("Training data loaded successfully")
    return data

def split_data(data: pd.DataFrame, target_col: str, test_size=0.2, random_state=42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Разделение данных на обучающую и тестовую выборки."""
    features = data.drop(columns=[target_col])
    target = data[target_col].astype('category').cat.codes if data[target_col].dtype in ['object', 'category'] else data[target_col]

    return train_test_split(features, target, test_size=test_size, random_state=random_state, stratify=target)

def hyperparams_selection(features_train: pd.DataFrame, features_test: pd.DataFrame, target_train: pd.Series, target_test: pd.Series, param_grid: Dict) -> Tuple[Dict, CatBoostClassifier]:
    """Выбор гиперпараметров с помощью GridSearchCV."""
    categorical_features = features_train.select_dtypes(include=['object', 'category']).columns.tolist()

    model = CatBoostClassifier(
        loss_function='MultiClass',
        eval_metric='MultiClass',
        custom_metric='Recall',
        verbose=0,
        random_seed=42
    )

    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='recall_macro',
        cv=3,
        verbose=1,
        n_jobs=-1
    )

    grid_search.fit(features_train, target_train, cat_features=categorical_features, eval_set=(features_test, target_test), verbose=0)

    return grid_search.best_params_, grid_search.best_estimator_

def save_json(path: str, data: Dict) -> None:
    """Сохранение данных в формате JSON."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_metrics(model: CatBoostClassifier, features_test: pd.DataFrame, target_test: pd.Series) -> Dict[str, float]:
    """Вычисление метрик для оценки модели."""
    target_pred = model.predict(features_test)
    target_pred_prob = model.predict_proba(features_test)

    metrics = {
        "accuracy": accuracy_score(target_test, target_pred),
        "f1_macro": f1_score(target_test, target_pred, average='macro'),
        "f1_weighted": f1_score(target_test, target_pred, average='weighted'),
        "roc_auc": roc_auc_score(target_test, target_pred_prob, multi_class="ovr", average="macro"),
        "recall": recall_score(target_test, target_pred, average="macro")
    }

    return metrics

def model_save(path: str, model: CatBoostClassifier) -> None:
    """Сохранение модели."""
    model.save_model(path)

def main() -> None:
    """Основная функция для запуска процесса."""
    target_column = 'target_class'
    param_grid = {
        'iterations': [100, 150],
        'depth': [2],
        'learning_rate': [0.01, 0.05],
        'l2_leaf_reg': [3],
        'border_count': [64]
    }

    args = parse_args()
    train_data = load_train_data(args.data_path)
    features_train, features_test, target_train, target_test = split_data(train_data, target_column)
    
    best_params, best_model = hyperparams_selection(features_train, features_test, target_train, target_test, param_grid)
    
    save_json(args.output_path, best_params)
    
    metrics = get_metrics(best_model, features _test, target_test)
    save_json(args.metrics, metrics)
    
    model_save('models/model.cbm', best_model)

if __name__ == '__main__':
    main()