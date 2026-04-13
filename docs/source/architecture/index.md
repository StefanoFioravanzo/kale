# Architecture

This page is a map of the Kale codebase — what the major components are,
how they fit together, and what each directory contains. It is aimed at
contributors who want to navigate the repo with confidence.

## The three layers

Kale has three layers that talk to each other:

1. **Backend (Python)** — the `kale/` package. Parses notebooks,
   compiles them to KFP v2 DSL, and invokes the KFP SDK to submit
   pipelines. This is also what `kale_server` exposes via JSON-RPC.
2. **Frontend (TypeScript / React)** — the `labextension/` package. A
   JupyterLab 4 extension that adds a Kale side panel and per-cell
   metadata editors.
3. **External** — the user's Kubeflow Pipelines cluster plus the
   Kubernetes API. Kale submits pipelines through the KFP SDK; it does not
   talk to Kubernetes directly unless a feature (like volume management)
   requires it.

```
  JupyterLab UI
       │
       │  JSON-RPC (kale_server)
       ▼
  ┌───────────────┐
  │ Kale backend  │ ─── compile notebooks, submit pipelines
  └───────────────┘
       │
       │  KFP SDK
       ▼
  Kubeflow Pipelines  ─── runs steps on Kubernetes
```

## Backend layout

The Python package lives at `kale/`. The interesting modules are:

### Core pipeline model

- `pipeline.py` — defines {py:class}`kale.pipeline.Pipeline` (a
  `networkx.DiGraph` of steps) along with the configuration classes
  {py:class}`~kale.pipeline.PipelineConfig`, `VolumeConfig`, and
  `KatibConfig`.
- `step.py` — defines {py:class}`kale.step.Step` and
  {py:class}`~kale.step.StepConfig`, plus the `PipelineParam` and
  `Artifact` named tuples used across the backend.

### Notebook processing

- `processors/nbprocessor.py` — {py:class}`kale.processors.NotebookProcessor`
  reads an `.ipynb`, parses tags, resolves data dependencies, and returns
  a ready-to-compile `Pipeline`.

### Compilation

- `compiler.py` — {py:class}`kale.compiler.Compiler` renders the
  templates in `kale/templates/` to produce KFP v2 DSL.
- `templates/nb_function_template.jinja2` — per-step component template.
- `templates/pipeline_template.jinja2` — pipeline wrapper template.

### Marshalling

- `marshal/backend.py` — {py:class}`~kale.marshal.backend.Dispatcher` and
  {py:class}`~kale.marshal.backend.MarshalBackend` base class.
- `marshal/backends.py` — nine concrete backends for numpy, pandas,
  sklearn, XGBoost, PyTorch, Keras, TensorFlow, functions, and a `dill`
  fallback.
- `marshal/decorator.py` — the `@marshal` decorator used by the marshal
  entrypoint.

### Static analysis

- `common/astutils.py` — AST helpers for detecting marshal candidates,
  parsing metrics print statements, and resolving imports.
- `common/flakeutils.py` — PyFlakes integration.

### KFP and Kubernetes integration

- `common/kfputils.py` — compile DSL, upload pipelines, create runs via
  the KFP SDK.
- `common/k8sutils.py`, `common/podutils.py` — K8s API helpers used by
  volume management and the in-pod runtime.
- `common/katibutils.py` — Katib hyperparameter tuning helpers (legacy,
  under re-evaluation for v2).

### Configuration framework

- `config/config.py` — a small Pydantic-inspired validation framework used
  by all the `*Config` classes in `pipeline.py` and `step.py`.
- `config/validators.py` — validators for Kubernetes names, image refs,
  and other common field types.

### CLI

- `cli.py` — three entry points declared in `pyproject.toml`:
  - `kale` — compile and run notebooks.
  - `kale_server` — JSON-RPC server used by the labextension.
  - `kale-volumes` — volume management helpers.

### RPC layer

- `rpc/nb.py` — notebook compilation RPC endpoints.
- `rpc/kfp.py` — KFP operations (upload, run, list experiments).
- `rpc/katib.py` — Katib operations.
- `rpc/run.py` — the JSON-RPC dispatcher.
- `rpc/errors.py` — error types (`RPCNotFoundError`, etc.).

## Frontend layout

The JupyterLab extension lives at `labextension/`. It's a standard
JupyterLab 4 extension built with TypeScript and React.

Key source files:

- `src/index.ts` — extension activation.
- `src/widget.tsx` — the main Kale left sidebar widget.
- `src/widgets/LeftPanel.tsx` — top-level panel with the master toggle,
  pipeline settings form, and Deploy button.
- `src/widgets/cell-metadata/CellMetadataEditor.tsx` — per-cell Kale row
  (cell type dropdown, step name, dependency picker).
- `src/widgets/deploys-progress/` — progress notifications for running
  deploys.
- `src/lib/RPCUtils.tsx` — JSON-RPC client for `kale_server`.
- `src/lib/CellUtils.ts`, `TagsUtils.ts`, `NotebookUtils.ts` — helpers for
  manipulating notebook metadata.
- `schema/kale-settings.json` — JupyterLab settings schema for any
  user-facing preferences.

The extension talks to the backend over JSON-RPC through a single shared
channel (`kale_server`), so every action the user takes in the UI maps to
a small set of backend calls.

## Data flow end-to-end

Putting all the pieces together, here's what happens when you click
**Compile and Run** in the Kale side panel on a notebook called
`my_notebook.ipynb`:

```
JupyterLab UI (React)
     │ RPCUtils.post("nb.compile_notebook", {path})
     ▼
kale_server (JSON-RPC)
     │ rpc/nb.compile_notebook()
     ▼
NotebookProcessor           ── parse tags, build Pipeline DAG
     │
     ▼
Compiler                    ── render Jinja templates, autopep8
     │
     ▼
.kale/my_notebook.kale.py   ── plain KFP v2 DSL
     │
     ▼
kfp.compiler.Compiler       ── compile DSL → YAML IR
     │
     ▼
KFP REST API                ── upload pipeline, create run
     │
     ▼
Kubeflow Pipelines          ── schedule step pods
     │
     ▼
Step pod                    ── load inputs, run user code, save outputs
```

The generated DSL is a normal KFP v2 pipeline — no runtime dependency on
Kale beyond the marshalling helper that lives inside each component. This
means a Kale-produced pipeline keeps running even if Kale is uninstalled,
and it can be inspected, edited, or re-uploaded by anyone with the KFP
SDK.
