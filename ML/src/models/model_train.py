import argparse
import json
import logging
from catboost import CatBoostClassifier
from hyperparams_selection import load_train_data

def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for the script.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Train classification model on best params")
    parser.add_argument("-d", "--dataset", required=True, help="Path to the dataset")
    parser.add_argument("-p", "--params", required=True, help="Path to the JSON file with model parameters")
    parser.add_argument("-o", "--output", required=True, help="Path to save the trained model")

    return parser.parse_args()

def load_params(params_path: str) -> dict:
    """
    Loads model parameters from a JSON file.

    Args:
        params_path (str): Path to the JSON file with model parameters.

    Returns:
        dict: A dictionary of model parameters.
    """
    with open(params_path, "r", encoding='utf-8') as file:
        params = json.load(file)
    
    logging.info("Model parameters loaded successfully")
    return params

def model_fit(params: dict, features: pd.DataFrame, target: pd.Series) -> CatBoostClassifier:
    """
    Initializes and trains a CatBoost classifier with the specified parameters.

    Args:
        params (dict): Parameters for initializing the CatBoostClassifier.
        features (pd.DataFrame): Features for training the model.
        target (pd.Series): Target variable (class labels).

    Returns:
        CatBoostClassifier: The trained CatBoost model.
    """
    model = CatBoostClassifier(**params)
    logging.info("CatBoost model initialized")
    
    categorical_features = features.select_dtypes(include=['object', 'category']).columns.tolist()
    model.fit(features, target, cat_features=categorical_features)
    
    logging.info("Model training completed")
    return model

def model_save(model: CatBoostClassifier, path: str) -> None:
    """
    Saves the trained model to the specified file.

    Args:
        model (CatBoostClassifier): The trained CatBoost model.
        path (str): Path to save the model.

    Returns:
        None
    """
    model.save_model(path)
    logging.info(f'Model saved successfully at: {path}')

def main() -> None:
    """Main function to execute the training process."""
    args = parse_args()

    # Load data and parameters
    data = load_train_data(args.dataset)
    target = data.pop('target_class')  # Efficiently drop and get target
    params = load_params(args.params)

    # Train the model and save it
    model = model_fit(params, data, target)
    model_save(model, args.output)

if __name__ == "__main__":
    main()