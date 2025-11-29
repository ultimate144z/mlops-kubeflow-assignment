from kfp import dsl
from kfp.compiler import Compiler
# Importing python functions directly prevents YAML version errors
from src.pipeline_components import (
    extract_data,
    preprocess_data,
    train_model,
    evaluate_model
)

@dsl.pipeline(
    name='Insurance Prediction ML Pipeline',
    description='End-to-end ML pipeline for medical insurance cost prediction'
)
def insurance_ml_pipeline():
    # Step 1: Extract data from DVC
    extract_task = extract_data()
    
    # Step 2: Preprocess data
    preprocess_task = preprocess_data(
        input_csv_path=extract_task.outputs['output_csv_path']
    )
    
    # Step 3: Train model
    train_task = train_model(
        X_train_path=preprocess_task.outputs['X_train_path'],
        y_train_path=preprocess_task.outputs['y_train_path']
    )
    
    # Step 4: Evaluate model
    evaluate_task = evaluate_model(
        X_test_path=preprocess_task.outputs['X_test_path'],
        y_test_path=preprocess_task.outputs['y_test_path'],
        model_path=train_task.outputs['model_output_path']
    )

if __name__ == '__main__':
    Compiler().compile(
        pipeline_func=insurance_ml_pipeline,
        package_path='pipeline.yaml'
    )
    print("✓ Pipeline compiled successfully to pipeline.yaml")