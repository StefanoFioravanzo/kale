# Quickstart

This walk-through takes you from a stock Kale install to a running pipeline
on Kubeflow Pipelines in under ten minutes, using the `candies_sharing`
example that ships with the repository.

## Prerequisites

Before you start, make sure you have:

- Kale installed (see [](installation.md)).
- A running Kubernetes cluster with Kubeflow Pipelines v2.16.0+ deployed.
- The KFP API reachable on `http://127.0.0.1:8080` — for a minikube setup you
  can run:
  ```bash
  kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
  ```

## 1. Open the example notebook

The `examples/base/candies_sharing.ipynb` notebook defines a toy pipeline that
demonstrates every Kale concept in the minimum amount of code. Open it in
JupyterLab:

```bash
make jupyter
# then browse to examples/base/candies_sharing.ipynb
```

The notebook is already annotated with Kale tags, so you can run Kale on it
without touching a thing.

## 2. Understand the cell tags

Open the Kale side panel (left sidebar → Kale icon → toggle on). You'll see
that each cell now has a dropdown showing its Kale cell type. The notebook
uses most of Kale's core tag types:

- **Imports** — all `import` statements go here. Kale prepends this cell to
  every step in the pipeline.
- **Pipeline Parameters** — defines values that will become KFP parameters,
  tweakable at submission time.
- **Step** — one or more named steps, each with optional dependencies on
  earlier steps (declared via `prev:<step_name>`).

See [](../concepts/cell-types.md) for the full tag vocabulary.

## 3. Compile the notebook

You can compile from the command line:

```bash
kale --nb examples/base/candies_sharing.ipynb
```

Kale will:

1. Parse the notebook and extract the Kale tags from cell metadata.
2. Build a pipeline DAG from the `step` and `prev:` annotations.
3. Detect which variables need to flow between steps.
4. Generate a KFP v2 DSL Python script next to the notebook.

## 4. Inspect the generated pipeline

Look inside the `.kale/` directory that was just created:

```bash
ls .kale/
# candies_sharing.kale.py     ← generated KFP v2 DSL
```

Open `candies_sharing.kale.py` — you'll see one `@kfp_dsl.component` function
per step, a `@kfp_dsl.pipeline` function wiring them together, and a
`__main__` block that you can run directly to compile the pipeline to YAML.

## 5. Submit the pipeline

Add `--run_pipeline` to compile **and** submit the pipeline to KFP in one
shot:

```bash
kale --nb examples/base/candies_sharing.ipynb \
     --kfp_host http://127.0.0.1:8080 \
     --run_pipeline
```

This uploads the pipeline, creates an experiment (default:
`Kale-Pipeline-Experiment`), and starts a run.

## 6. Watch it run

Open the KFP UI at <http://127.0.0.1:8080> and navigate to **Runs**. You
should see your new run executing step-by-step. Click a step to see its
logs, artifacts, and the data Kale marshalled in and out of it.

## What's next?

- Kale is available **directly inside JupyterLab** via the Deploy button in
  the side panel — see [](../user-guide/running-pipelines.md).
- Learn how Kale detects and moves data between steps in
  [](../concepts/data-passing.md).
- Browse the [](../examples.md) gallery for more realistic pipelines.
