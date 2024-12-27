import argparse
import pandas as pd
from catboost import CatBoostClassifier

def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for the script.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Launch CatBoost model and predict")
    
    parser.add_argument("-m", "--model_path", required=True, help="Path to the trained model file")
    parser.add_argument("-d", "--data_path", required=True, help="Path to the prepared data for prediction")
    parser.add_argument("-o", "--output_path", required=True, help="Path to save the predictions")
    parser.add_argument("-p", "--probabilities", action="store_true", help="Flag for predicting probabilities")

    return parser.parse_args()

def load_model(model_path: str) -> CatBoostClassifier:
    """
    Loads a pre-trained CatBoost model from the specified path.

    Args:
        model_path (str): Path to the model file.

    Returns:
        CatBoostClassifier: Loaded CatBoost model.
    """
    model = CatBoostClassifier()
    model.load_model(model_path)
    return model

def predict(model: CatBoostClassifier, data: pd.DataFrame, probabilities: bool) -> pd.DataFrame:
    """
    Predicts class labels or probabilities for the provided data using the loaded model.

    Args:
        model (CatBoostClassifier): The loaded CatBoost model.
        data (pd.DataFrame): Data for prediction.
        probabilities (bool): If True, predicts probabilities instead of class labels.

    Returns:
        pd.DataFrame: DataFrame containing predictions or probabilities.
    """
    if probabilities:
        predictions = model.predict_proba(data)
    else:
        predictions = model.predict(data)

    return pd.DataFrame(predictions, columns=["prediction"])

def main() -> None:
    """Main function to execute the prediction process."""
    args = parse_args()
    model = load_model(args.model_path)
    data = pd.read_csv(args.data_path)

    # Drop unnecessary columns if they exist
    data.drop(columns=[col for col in ['target_class', 'target_reg'] if col in data.columns], inplace=True)

    # Get predictions
    output_df = predict(model, data, args.probabilities)

    # Save predictions to CSV
    output_df.to_csv(args.output_path, index=False)
    print(f"Predictions saved to: {args.output_path}")

if __name__ == '__main__':
    main()