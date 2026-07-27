# Import libraries
import joblib
import optuna
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor


# Load data
df = pd.read_csv("r_insurance3.csv")
print(df.head())

# Basic EDA
print(df.info())
print(df.describe())

# Features and target
categorical = ["sex", "smoker", "region"]
numerical = ["age", "bmi", "children"]
target = "charges"

X = df.drop(columns=target)
y = df[target]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Preprocessor
preprocessor = ColumnTransformer([
    ("ohe", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical),
    ("scale", MinMaxScaler(), numerical)
])

# Model
xgb = XGBRegressor(
    n_estimators=167,
    learning_rate=0.01,
    max_depth=6,
    random_state=42
)

# Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", xgb)
])

# Train
pipeline.fit(X_train, y_train)

# Predict
xgb_pred = pipeline.predict(X_test)

# Evaluation
def evaluate(y_true, y_pred, name):
    print(name)
    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("R² Score:", r2_score(y_true, y_pred))
    print()

evaluate(y_test, xgb_pred, "XGBoost")

# Feature names
feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

# XGBoost Optuna
def xgb_objective(trial):

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", XGBRegressor(
            n_estimators=trial.suggest_int("n_estimators", 100, 300),
            max_depth=trial.suggest_int("max_depth", 3, 10),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
            subsample=trial.suggest_float("subsample", 0.5, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.5, 1.0),
            random_state=42
        ))
    ])

    return cross_val_score(model, X, y, cv=5, scoring="r2").mean()

# Save pipeline
joblib.dump(pipeline, "model.pkl")
print("Pipeline saved successfully.")