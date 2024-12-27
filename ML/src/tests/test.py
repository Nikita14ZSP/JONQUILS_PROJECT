import pandas as pd
import argparse
from sklearn.metrics import accuracy_score, f1_score

# Пороговые значения для метрик
ACCURACY_THRESHOLD = 0.9
F1_THRESHOLD = 0.8

def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Evaluate model predictions against ground truth.")
    parser.add_argument('-p', '--predictions', required=True, help="Path to the predictions CSV file.")
    parser.add_argument('-t', '--test', required=True, help="Path to the ground truth CSV file.")
    return parser.parse_args()

def evaluate_model(pred_path: str, real_path: str) -> None:
    """Оценивает модель, сравнивая предсказания с истинными значениями."""
    predicted = pd.read_csv(pred_path)
    real = pd.read_csv(real_path)

    # Вычисление метрик
    accuracy = accuracy_score(real['target_class'], predicted)
    f1_macro = f1_score(real['target_class'], predicted, average='macro')

    # Проверка на соответствие порогам
    if accuracy < ACCURACY_THRESHOLD:
        raise ValueError(f"Accuracy {accuracy:.2f} ниже порога {ACCURACY_THRESHOLD:.2f}")
    if f1_macro < F1_THRESHOLD:
        raise ValueError(f"F1 {f1_macro:.2f} ниже порога {F1_THRESHOLD:.2f}")

    print("Tests passed!")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"F1: {f1_macro:.2f}")

if __name__ == "__main__":
    args = parse_args()
    evaluate_model(args.predictions, args.test)