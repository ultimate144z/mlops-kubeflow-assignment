# compile_components.py

from kfp.compiler import Compiler
from pipeline_components import (
    extract_data,
    preprocess_data,
    train_model,
    evaluate_model
)


def compile_all():
    print("🔧 Compiling components into YAML...")

    # Compile each component directly (no wrapper pipelines needed)
    Compiler().compile(
        pipeline_func=extract_data,
        package_path="components/extract_data.yaml"
    )

    Compiler().compile(
        pipeline_func=preprocess_data,
        package_path="components/preprocess_data.yaml"
    )

    Compiler().compile(
        pipeline_func=train_model,
        package_path="components/train_model.yaml"
    )

    Compiler().compile(
        pipeline_func=evaluate_model,
        package_path="components/evaluate_model.yaml"
    )

    print("✓ All component YAML files generated successfully.")


if __name__ == "__main__":
    compile_all()