# Examples

Kale ships with a gallery of example notebooks in the `examples/` directory
of the repository. Each example is self-contained and demonstrates a
different set of Kale features.

| Example | Directory | What it shows |
| ------- | --------- | ------------- |
| **Candies sharing** | [`examples/base/`](https://github.com/kubeflow/kale/tree/main/examples/base) | The simplest possible Kale pipeline. Good starting point for the [](getting-started/quickstart.md). |
| **Titanic ML dataset** | [`examples/titanic-ml-dataset/`](https://github.com/kubeflow/kale/tree/main/examples/titanic-ml-dataset) | Classic binary classification on the Titanic dataset. Demonstrates data loading, feature engineering, training, and evaluation steps. |
| **Taxi cab classification** | [`examples/taxi-cab-classification/`](https://github.com/kubeflow/kale/tree/main/examples/taxi-cab-classification) | Taxi fare prediction pipeline with a multi-stage preprocessing flow. |
| **PyTorch classification** | [`examples/pytorch-classification/`](https://github.com/kubeflow/kale/tree/main/examples/pytorch-classification) | Training a PyTorch image classifier. Shows Kale's PyTorch marshalling backend in action. |
| **Dog breed classification** | [`examples/dog-breed-classification/`](https://github.com/kubeflow/kale/tree/main/examples/dog-breed-classification) | Transfer-learning image classification pipeline. |
| **OpenVaccine Kaggle competition** | [`examples/openvaccine-kaggle-competition/`](https://github.com/kubeflow/kale/tree/main/examples/openvaccine-kaggle-competition) | End-to-end Kaggle-style workflow with GNNs. |
| **Serving** | [`examples/serving/`](https://github.com/kubeflow/kale/tree/main/examples/serving) | Kale pipeline that trains a model and then serves it — demonstrates integration with model serving components. |

## Running an example

All examples follow the same pattern:

```bash
kale --nb examples/titanic-ml-dataset/titanic_dataset_ml.ipynb \
     --kfp_host http://127.0.0.1:8080 \
     --run_pipeline
```

The first run will bake all the Python dependencies into each step's
`packages_to_install` list, so the first step may take a minute or two to
start while pip installs the requirements inside the container.

## External tutorials

- **KubeCon NA Tutorial 2019** — *From Notebook to Kubeflow Pipelines: An
  End-to-End Data Science Workflow*. [Slides](https://kccncna19.sched.com/event/Uaeq/tutorial-from-notebook-to-kubeflow-pipelines-an-end-to-end-data-science-workflow-michelle-casbon-google-stefano-fioravanzo-fondazione-bruno-kessler-ilias-katsakioris-arrikto) ·
  [Video](https://www.youtube.com/watch?v=C9rJzTzVzvQ)
- **KubeCon EU Tutorial 2020** — *From Notebook to Kubeflow Pipelines with
  HP Tuning: A Data Science Journey*. [Slides](https://kccnceu20.sched.com/event/ZerG/tutorial-from-notebook-to-kubeflow-pipelines-with-hp-tuning-a-data-science-journey-stefano-fioravanzo-ilias-katsakioris-arrikto) ·
  [Video](https://www.youtube.com/watch?v=QK0NxhyADpM)
- **Kale introduction blog post** —
  [Automating Jupyter Notebook Deployments to Kubeflow Pipelines with Kale](https://medium.com/kubeflow/automating-jupyter-notebook-deployments-to-kubeflow-pipelines-with-kale-a4ede38bea1f)
- **Kale v2.0 demo video** —
  [YouTube](https://www.youtube.com/watch?v=UGLJuqJqJYY)
