# Testing Kale builds against Kubeflow Pipelines when devpi is required

The local devpi helpers in `backend/scripts/` make it easy to publish a dev build
of Kale and bake the `KALE_DEVPI_SIMPLE_URL` into generated components. When the
Kubeflow Pipelines (KFP) runtime runs inside Kubernetes, the pods must be able
to reach that devpi instance. Two practical workflows are described below.

## Option A – Reuse a devpi running on your laptop/workstation

This approach keeps the disposable index on your machine and exposes it to the
cluster:

1. Start devpi so it listens on all interfaces and record the URL:

   ```bash
   cd backend
   HOST=0.0.0.0 PORT=3141 source scripts/devpi-main.sh
   # KALE_DEVPI_SIMPLE_URL now points to http://<host>:3141/root/dev/simple/
   ```

2. Find an address that Kubernetes pods can use to reach your host:

   - **kind / Docker Desktop:** `host.docker.internal` usually resolves from a
     pod; otherwise check the Docker network gateway (`docker network inspect
     kind | jq -r '.[0].IPAM.Config[0].Gateway'`).
   - **k3d:** `host.k3d.internal` or the gateway from `docker network inspect
     k3d`.
   - **minikube:** get the host node IP via `minikube ssh "ip route"` and look
     for the default gateway (often `192.168.49.1`).

   Validate from inside the cluster:

   ```bash
   kubectl run --rm -i --tty devpi-test \
     --image=curlimages/curl --restart=Never \
     --command -- sh -c "curl -I http://<host-ip>:3141/"
   ```

3. Export the reachable URL for component generation:

   ```bash
   export KALE_DEVPI_SIMPLE_URL="http://<host-ip>:3141/root/dev/simple/"
   KALE_DEV_MODE=1 kale --nb <notebook> --dev
   ```

   The generated KFP component will now install Kale from your workstation.

> For remote clusters you can tunnel the port instead: e.g. `ssh -R
> 3141:localhost:3141 user@bastion` and point `KALE_DEVPI_SIMPLE_URL` at the
> bastion host reachable from the cluster.

## Option B – Deploy devpi inside the Kubernetes cluster

Running devpi next to KFP avoids host-network gymnastics and gives the pods a
stable in-cluster URL.

1. Apply the provided manifest (creates a namespace, deployment, PVC, and
   ClusterIP service):

   ```bash
   kubectl apply -f backend/scripts/devpi-k8s.yaml
   ```

2. Forward the service locally to publish your build into the cluster-side index:

   ```bash
   kubectl -n devpi port-forward service/devpi 3141:3141
   cd backend
   KALE_DEV_MODE=1 KALE_DEVPI_SIMPLE_URL=http://localhost:3141/root/dev/simple/ \
     ./scripts/devpi-publish.sh
   ```

3. Point Kale’s generator at the in-cluster address that pods will use:

   ```bash
   export KALE_DEV_MODE=1
   export KALE_DEVPI_SIMPLE_URL="http://devpi.devpi.svc.cluster.local:3141/root/dev/simple/"
   kale --nb <notebook> --dev
   ```

4. After testing, tear down the helper resources:

   ```bash
   kubectl delete -f backend/scripts/devpi-k8s.yaml
   ```

Either option keeps the devpi flow introduced in PR #491 while ensuring the KFP
pods can actually resolve and download the dev build of Kale.
