# Main Kubeflow pipeline definition will go here
import kfp
from kfp import dsl

# 1. Load Components from YAML files
def load_components():
    extract_op = kfp.components.load_component_from_file('components/extract_data.yaml')
    preprocess_op = kfp.components.load_component_from_file('components/preprocess_data.yaml')
    train_op = kfp.components.load_component_from_file('components/train_model.yaml')
    evaluate_op = kfp.components.load_component_from_file('components/evaluate_model.yaml')
    return extract_op, preprocess_op, train_op, evaluate_op

# 2. Define the Pipeline
@dsl.pipeline(
    name='Insurance Prediction Pipeline',
    description='A pipeline that extracts, preprocesses, trains, and evaluates a model.'
)
def insurance_pipeline():
    extract_op, preprocess_op, train_op, evaluate_op = load_components()

    # Step 1: Extract
    extract_task = extract_op()

    # Step 2: Preprocess (Takes data from Extract)
    preprocess_task = preprocess_op(
        input_data=extract_task.output
    )

    # Step 3: Train (Takes data from Preprocess)
    train_task = train_op(
        processed_data=preprocess_task.output
    )

    # Step 4: Evaluate (Takes model from Train and data from Preprocess)
    evaluate_task = evaluate_op(
        model=train_task.outputs['model_output'],
        test_data=preprocess_task.output
    )

# 3. Compiler Step (CRITICAL for Task 4)
if __name__ == '__main__':
    import kfp.compiler as compiler
    print("Compiling pipeline...")
    compiler.Compiler().compile(insurance_pipeline, 'pipeline.yaml')
    print("SUCCESS: pipeline.yaml generated.")