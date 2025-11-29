# MLOps Pipeline with Kubeflow, DVC, and GitHub Actions

## Project Overview
This project implements an end-to-end Machine Learning Operations (MLOps) pipeline for Medical Insurance Cost Prediction. The goal is to predict individual medical insurance charges based on features like age, sex, bmi, children, smoker status, and region.

The pipeline is designed to ensure reproducibility, automation, and scalability using industry-standard tools:
* Data Versioning: DVC (Data Version Control) to track dataset changes.
* Orchestration: Kubeflow Pipelines (KFP) on Minikube to manage the ML workflow.
* CI/CD: GitHub Actions to automate pipeline compilation and testing.

### The ML Pipeline Steps
1.  Data Extraction: Fetches versioned data from DVC storage.
2.  Preprocessing: Cleans data, encodes categorical variables, and splits into train/test sets.
3.  Model Training: Trains a Linear Regression model using Scikit-learn.
4.  Evaluation: Calculates metrics (MAE, MSE, R2 Score) to assess model performance.

---

## Setup Instructions

### 1. Prerequisites
Ensure you have the following installed:
* Docker Desktop: https://www.docker.com/
* Minikube: https://minikube.sigs.k8s.io/docs/start/
* Python 3.8+: https://www.python.org/
* Kubectl: https://kubernetes.io/docs/tasks/tools/

### 2. Repository Setup
Clone the repository and install dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/mlops-kubeflow-assignment.git
cd mlops-kubeflow-assignment
pip install -r requirements.txt
```

### 3. DVC Setup (Data Versioning)
The dataset is tracked using DVC. To fetch the data:

```bash
# Pull the latest data from the configured remote storage
dvc pull
```
Note: The raw data is stored in `data/insurance.csv`.

### 4. Infrastructure Setup (Minikube & Kubeflow)
Start the local Kubernetes cluster:

```bash
minikube start --cpus=4 --memory=7000 --disk-size=20g --driver=docker
```

Deploy Kubeflow Pipelines (Standalone):

```bash
export PIPELINE_VERSION=2.0.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

## Pipeline Walkthrough

### 1. Compile the Pipeline
The pipeline logic is defined in `pipeline.py`. To compile it into a Kubernetes-compatible YAML file:

```bash
python pipeline.py
# Output: pipeline.yaml will be generated in the root directory.
```

### 2. Run on Kubeflow Dashboard
Port Forward the Dashboard:

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Access the UI: Open http://localhost:8080 in your browser.

Upload Pipeline: Click "Upload Pipeline" and select the generated `pipeline.yaml`.

Create Run: Click "Create Run" to execute the pipeline steps.

## Continuous Integration (CI)
This repository uses GitHub Actions to automate quality checks. On every push to the main branch, the workflow:

- Sets up a Python environment.
- Installs dependencies (kfp, pandas, etc.).
- Compiles the pipeline code to ensure there are no syntax errors.

Workflow file: `.github/workflows/main.yml`

## Known Issues & Workarounds

**Network Constraints on Google Container Registry (gcr.io)**

During the deployment of Task 3, the local network environment blocked connections to gcr.io, preventing the official Kubeflow UI images from downloading (ErrImagePull).

**Resolution/Workaround:** To demonstrate successful orchestration and service exposure capabilities despite this infrastructure limitation:

- The deployment was patched to use standard, verified images (Nginx and Minio) from Docker Hub.
- The cluster status and service exposure were verified via `kubectl get pods` and browser access to the exposed service.
- The pipeline logic itself (`pipeline.py`) remains fully implemented and compiles successfully via the CI pipeline.