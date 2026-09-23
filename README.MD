# Kubernetes Mini Project — Notes API

A hands-on Kubernetes project built to practice **Kubernetes administration, troubleshooting, and CKA-oriented concepts** while deploying a containerized Flask Notes API.

The project is being developed incrementally, with **Git/GitHub maintained alongside the Kubernetes work**.

---

## 🎯 Project Goals

This project is designed to provide practical experience with:

* Dockerized Flask applications
* Kubernetes Namespaces
* Pods
* Deployments
* ReplicaSets
* Labels and selectors
* Desired vs actual state
* Scaling
* Self-healing
* Rolling Updates
* Rollout status and history
* Rollbacks
* Deployment troubleshooting
* Image pull failures
* Kubernetes debugging using `kubectl`
* Git and GitHub workflow

---

## 🏗️ Application Architecture

```text
                    Kubernetes Cluster
                           │
                           ▼
                  ┌─────────────────┐
                  │   notes-app     │
                  │   Namespace     │
                  └────────┬────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Deployment  │
                    │ notes-app    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ ReplicaSet  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           Pod 1         Pod 2        Pod 3
              │            │            │
              └────────────┼────────────┘
                           ▼
                    Flask Notes API
```

---

## 📁 Project Structure

```text
k8s-mini-project/
│
├── .gitignore
├── README.md
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── k8s/
    ├── namespace.yaml
    └── deployment.yaml
```

---

# 🐍 Flask Application

The application is a simple Notes API built using Flask.

### Endpoints

| Endpoint  | Description             |
| --------- | ----------------------- |
| `/`       | Application information |
| `/health` | Health check            |
| `/notes`  | Returns sample notes    |

The application runs on:

```text
0.0.0.0:5000
```

---

# 🐳 Docker

The Flask application is containerized using Docker.

### Docker image

```text
notes-app:v1
```

The image was built locally and loaded into the Kind cluster.

```bash
kind load docker-image notes-app:v1 --name k8s-lab
```

The Kubernetes Deployment uses:

```yaml
image: notes-app:v1
imagePullPolicy: IfNotPresent
```

Using `IfNotPresent` allows Kubernetes to use the image already loaded into the Kind node instead of unnecessarily trying to pull it from a registry.

---

# ☸️ Kubernetes

## 1. Namespace

The application runs inside its own namespace:

```text
notes-app
```

Namespace definition:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: notes-app
```

The namespace provides a logical boundary for the project's Kubernetes resources.

Commands:

```bash
kubectl get namespaces
kubectl get pods -n notes-app
kubectl get deployment -n notes-app
kubectl get rs -n notes-app
```

---

# 2. Deployment

The application is managed using a Kubernetes Deployment.

Current configuration:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: notes-app
  namespace: notes-app

spec:
  replicas: 3

  selector:
    matchLabels:
      app: notes-app

  template:
    metadata:
      labels:
        app: notes-app

    spec:
      containers:
        - name: notes-app
          image: notes-app:v1
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 5000
```

The Deployment maintains a desired state of:

```text
3 replicas
```

---

# 3. Deployment → ReplicaSet → Pods

A key Kubernetes relationship practiced in this project:

```text
Deployment
    ↓
ReplicaSet
    ↓
Pods
    ↓
Containers
```

The Deployment manages the ReplicaSet.

The ReplicaSet ensures that the required number of Pods exists.

For example:

```text
Deployment: notes-app
        │
        ▼
ReplicaSet: notes-app-5dc76bfb98
        │
        ├── Pod
        ├── Pod
        └── Pod
```

---

# 4. Labels and Selectors

The Deployment uses:

```yaml
selector:
  matchLabels:
    app: notes-app
```

The Pod template contains:

```yaml
labels:
  app: notes-app
```

The selector allows the Deployment to identify which Pods belong to it.

---

# 5. Scaling

Kubernetes allows the desired number of replicas to be changed.

Example:

```bash
kubectl scale deployment notes-app --replicas=5 -n notes-app
```

The ReplicaSet then creates or removes Pods until the actual state matches the desired state.

Important concept:

> Changing the number of replicas does not change the Pod template, so it does not create a new ReplicaSet.

---

# 6. Self-Healing

ReplicaSets continuously try to maintain the desired number of Pods.

For example:

```text
Desired: 3 Pods

Pod 1 ✅
Pod 2 ✅
Pod 3 ❌
```

The ReplicaSet detects the difference and creates a replacement:

```text
Pod 1 ✅
Pod 2 ✅
Pod 4 ✅
```

This demonstrates Kubernetes' desired-state model.

---

# 🔄 Rolling Updates

A Deployment can update Pods gradually instead of replacing everything at once.

For example:

```text
v1   v1   v1
 ↓
v1   v1   v2
 ↓
v1   v2   v2
 ↓
v2   v2   v2
```

This process is called a **rollout**.

The default Deployment strategy is:

```text
RollingUpdate
```

The important idea is:

> A rollout is the process of moving a Deployment from its old Pod template to a new Pod template.

---

# 🧬 Pod Template Hash

When the Pod template changes, Kubernetes creates a new ReplicaSet.

For example:

```text
Old:
notes-app-5dc76bfb98

New:
notes-app-57887f88bf
```

The hash identifies the Pod template version.

Changing only:

```yaml
replicas: 3
```

does not create a new ReplicaSet.

Changing something inside:

```yaml
spec:
  template:
```

can create a new ReplicaSet.

Examples include:

* Container image
* Container port
* Environment variables
* Resource configuration
* Pod template labels

---

# 🚨 Failed Rollout Troubleshooting

The project intentionally tested a failed deployment.

The image was changed from:

```yaml
image: notes-app:v1
```

to:

```yaml
image: notes-app:v1_notPresent
```

Kubernetes created a new ReplicaSet and attempted to start a new Pod.

The new Pod entered:

```text
ErrImagePull
```

and later:

```text
ImagePullBackOff
```

The old healthy Pods remained running because Kubernetes could not successfully bring up the new version.

The troubleshooting chain used was:

```text
Deployment
    ↓
ReplicaSet
    ↓
Pod
    ↓
kubectl describe pod
    ↓
Events
    ↓
Image pull failure
```

Useful command:

```bash
kubectl describe pod <pod-name> -n notes-app
```

The Events section showed:

```text
Failed to pull image "notes-app:v1_notPresent"
```

followed by:

```text
ErrImagePull
```

and:

```text
ImagePullBackOff
```

### Difference

**ErrImagePull**

> Kubernetes initially failed to pull the image.

**ImagePullBackOff**

> Kubernetes continues retrying the image pull, but waits progressively longer between attempts.

---

# 📊 Rollout Status

To check whether the Deployment's current update has completed:

```bash
kubectl rollout status deployment/notes-app -n notes-app
```

Example during the failed rollout:

```text
Waiting for deployment "notes-app" rollout to finish:
1 out of 3 new replicas have been updated...
```

This indicates that the Deployment has started the rollout but has not successfully completed it.

---

# 📜 Rollout History

Deployment revisions can be inspected with:

```bash
kubectl rollout history deployment/notes-app -n notes-app
```

A specific revision can be inspected with:

```bash
kubectl rollout history deployment/notes-app --revision=<revision-number> -n notes-app
```

### Important

Because the Deployment exists inside the `notes-app` namespace, the namespace must be specified:

```bash
-n notes-app
```

Without it, `kubectl` searches the default namespace.

---

# ↩️ Rollback

A Deployment can be rolled back to a previous revision:

```bash
kubectl rollout undo deployment/notes-app -n notes-app
```

A specific revision can be selected:

```bash
kubectl rollout undo deployment/notes-app --to-revision=<revision-number> -n notes-app
```

Rollback is itself a new Deployment rollout using the previous Pod template.

---

# 🔍 Important Troubleshooting Commands

### Check Pods

```bash
kubectl get pods -n notes-app
```

### Detailed Pod information

```bash
kubectl describe pod <pod-name> -n notes-app
```

### Check Deployment

```bash
kubectl get deployment -n notes-app
```

### Check ReplicaSets

```bash
kubectl get rs -n notes-app
```

### Check rollout status

```bash
kubectl rollout status deployment/notes-app -n notes-app
```

### Check rollout history

```bash
kubectl rollout history deployment/notes-app -n notes-app
```

### Check a specific revision

```bash
kubectl rollout history deployment/notes-app --revision=<revision-number> -n notes-app
```

### Rollback

```bash
kubectl rollout undo deployment/notes-app -n notes-app
```

---

# 🔧 Git Workflow

Git is maintained alongside the Kubernetes project.

Basic workflow:

```text
Make change
    ↓
git status
    ↓
git diff
    ↓
git add .
    ↓
git commit
    ↓
git push
    ↓
GitHub
```

Useful commands:

```bash
git status
git diff
git add .
git commit -m "message"
git push
git pull
git log --oneline
```

The project uses GitHub to track the evolution of the Kubernetes configuration and application code.

---

# 🧪 Current Learning Status

### Completed

* [x] Flask Notes API
* [x] Dockerfile
* [x] Docker image
* [x] Kind cluster
* [x] Kubernetes Namespace
* [x] Deployment
* [x] ReplicaSet
* [x] Pods
* [x] Labels and selectors
* [x] Scaling
* [x] Self-healing
* [x] Pod-template hash
* [x] Rolling Updates
* [x] Rollout status
* [x] Rollout history
* [x] Failed rollout simulation
* [x] `ErrImagePull`
* [x] `ImagePullBackOff`
* [x] Pod troubleshooting with `kubectl describe`
* [x] Git/GitHub workflow

### Next

* [ ] Recover the failed rollout
* [ ] Practice rollback hands-on
* [ ] Kubernetes Service
* [ ] Service discovery
* [ ] ConfigMaps
* [ ] Secrets
* [ ] Resource requests and limits
* [ ] Probes
* [ ] Persistent storage
* [ ] Ingress
* [ ] More CKA troubleshooting scenarios

---

# 🎯 Project Objective

The goal is not just to deploy an application.

The goal is to understand how Kubernetes behaves when things **work, fail, and need to be recovered**.

The project will progressively evolve into a production-style Kubernetes deployment while documenting the learning process through Git and GitHub.
