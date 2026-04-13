# CLI Reference

Kale ships three command-line entry points, declared as `[project.scripts]`
in `pyproject.toml`:

| Command        | Purpose                                                       |
| -------------- | ------------------------------------------------------------- |
| `kale`         | Compile (and optionally run) a notebook against KFP.          |
| `kale_server`  | JSON-RPC server used by the JupyterLab extension.             |
| `kale-volumes` | Helpers for managing the PVCs Kale attaches to pipeline steps. |

## `kale`

The primary CLI. Parses a notebook, builds the pipeline DAG, compiles it to
KFP v2 DSL, and optionally uploads and runs it.

```bash
kale --nb path/to/notebook.ipynb [options]
```

### General options

| Flag                  | Type   | Description                                                          |
| --------------------- | ------ | -------------------------------------------------------------------- |
| `--nb`                | str    | Path to the source notebook. **Required.**                           |
| `--upload_pipeline`   | flag   | Upload the compiled pipeline to KFP.                                 |
| `--run_pipeline`      | flag   | Upload and then create a KFP run.                                    |
| `--debug`             | flag   | Enable verbose logging.                                              |
| `--dev`               | flag   | Bake a local devpi index URL into generated components.              |
| `--pip-index-urls`    | str    | Comma-separated PEP 503 simple indexes baked into components.        |
| `--devpi-simple-url`  | str    | Devpi simple URL (used when `--dev` is set).                         |

### Notebook metadata overrides

All the flags in this group override the corresponding fields in the
notebook's Kale metadata. If both are set, the CLI value wins.

| Flag                      | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `--experiment_name`       | KFP experiment name. Default: `Kale-Pipeline-Experiment`.    |
| `--pipeline_name`         | Name of the deployed pipeline. Default: `kale-pipeline`.     |
| `--pipeline_description`  | Description shown in the KFP UI.                             |
| `--docker_image`          | Default base image for every step.                           |
| `--kfp_host`              | KFP API endpoint, as `<host>:<port>` or a full URL.          |
| `--storage-class-name`    | Storage class for pipeline-created volumes.                  |
| `--volume-access-mode`    | Access mode for pipeline-created volumes.                    |

### Examples

Compile only, leave the generated script in `.kale/`:

```bash
kale --nb examples/base/candies_sharing.ipynb
```

Compile, upload, and run on a local KFP port-forward:

```bash
kale --nb examples/base/candies_sharing.ipynb \
     --kfp_host http://127.0.0.1:8080 \
     --run_pipeline
```

Override pipeline naming:

```bash
kale --nb notebooks/my_pipeline.ipynb \
     --pipeline_name "weekly-churn" \
     --experiment_name "production" \
     --run_pipeline --kfp_host http://127.0.0.1:8080
```

## `kale_server`

Starts the JSON-RPC server that the JupyterLab extension talks to. You
normally don't run this by hand — JupyterLab spawns it as a subprocess
when the Kale panel is activated. It's documented here for completeness.

```bash
kale_server
```

The server is implemented in `kale/rpc/` and exposes endpoints for
compiling notebooks, uploading pipelines, creating runs, listing
experiments, and a few Katib helpers.

## `kale-volumes`

Helper CLI for managing the volumes Kale attaches to pipeline steps.
Useful in multi-user clusters where data volumes are managed externally.
Run `kale-volumes --help` for the current subcommand list.

## Environment variables

A few environment variables affect `kale` and `kale_server`:

| Variable                  | Effect                                                                                 |
| ------------------------- | -------------------------------------------------------------------------------------- |
| `KF_PIPELINES_ENDPOINT`   | Default KFP API endpoint when `--kfp_host` is not provided.                            |
| `KF_PIPELINES_UI_ENDPOINT` | KFP UI URL used when rendering run links.                                             |
| `KALE_PIP_INDEX_URLS`     | Comma-separated list of pip indexes baked into generated components.                   |
| `KALE_PIP_TRUSTED_HOSTS`  | Trusted hosts for HTTP pip indexes (required when using HTTP URLs).                    |
| `KALE_DEV_MODE`           | Equivalent to passing `--dev`.                                                         |
| `KALE_DEVPI_SIMPLE_URL`   | Equivalent to `--devpi-simple-url` when `--dev` is set.                                |

See [](../user-guide/running-pipelines.md) for concrete scenarios where
these are useful.
