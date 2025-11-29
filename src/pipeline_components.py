# pipeline_components.py

from kfp import dsl

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn", "dvc"]
)
def extract_data(output_csv_path: dsl.OutputPath(str)):
    """Extract data from DVC and save to CSV."""
    import pandas as pd
    import subprocess
    
    print("Running DVC pull to fetch dataset...")
    subprocess.run(["dvc", "pull"], check=True)
    
    df = pd.read_csv("data/insurance.csv")
    print(f"✓ Data extracted: {df.shape[0]} rows, {df.shape[1]} columns")
    
    with open(output_csv_path, 'w') as f:
        df.to_csv(f, index=False)


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn"]
)
def preprocess_data(
    input_csv_path: dsl.InputPath(str),
    X_train_path: dsl.OutputPath(str),
    X_test_path: dsl.OutputPath(str),
    y_train_path: dsl.OutputPath(str),
    y_test_path: dsl.OutputPath(str)
):
    """Preprocess the data and split into train/test sets."""
    import pandas as pd
    import pickle
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    
    df = pd.read_csv(input_csv_path)
    
    # Encode categorical variables
    label_encoders = {}
    for col in ['sex', 'smoker', 'region']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    X = df.drop('charges', axis=1)
    y = df['charges']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Save outputs
    with open(X_train_path, 'wb') as f:
        pickle.dump(X_train, f)
    with open(X_test_path, 'wb') as f:
        pickle.dump(X_test, f)
    with open(y_train_path, 'wb') as f:
        pickle.dump(y_train, f)
    with open(y_test_path, 'wb') as f:
        pickle.dump(y_test, f)
    
    print(f"✓ Data preprocessed: {X_train.shape[0]} train, {X_test.shape[0]} test samples")


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn"]
)
def train_model(
    X_train_path: dsl.InputPath(str),
    y_train_path: dsl.InputPath(str),
    model_output_path: dsl.OutputPath(str)
):
    """Train a Linear Regression model."""
    import pickle
    from sklearn.linear_model import LinearRegression
    
    with open(X_train_path, 'rb') as f:
        X_train = pickle.load(f)
    with open(y_train_path, 'rb') as f:
        y_train = pickle.load(f)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    with open(model_output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print("✓ Model trained successfully")


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn"]
)
def evaluate_model(
    X_test_path: dsl.InputPath(str),
    y_test_path: dsl.InputPath(str),
    model_path: dsl.InputPath(str),
    metrics_output_path: dsl.OutputPath(str)
):
    """Evaluate the model and save metrics."""
    import pickle
    import json
    from sklearn.metrics import mean_squared_error, r2_score
    
    with open(X_test_path, 'rb') as f:
        X_test = pickle.load(f)
    with open(y_test_path, 'rb') as f:
        y_test = pickle.load(f)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    y_pred = model.predict(X_test)
    
    metrics = {
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': mean_squared_error(y_test, y_pred, squared=False),
        'r2': r2_score(y_test, y_pred)
    }
    
    with open(metrics_output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✓ Model evaluated - RMSE: {metrics['rmse']:.2f}, R²: {metrics['r2']:.4f}")