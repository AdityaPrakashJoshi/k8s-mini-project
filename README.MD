# Kubernetes Mini Project — Notes API

A hands-on Kubernetes project built to practice core Kubernetes and DevOps concepts while preparing for the **CKA (Certified Kubernetes Administrator)** exam.

The project starts with a simple Flask Notes API, containerizes it with Docker, and progressively deploys and manages it on Kubernetes.

## 🎯 Project Goals

* Build and containerize a simple web application
* Deploy the application to Kubernetes
* Understand the relationship between:

  * Deployment
  * ReplicaSet
  * Pod
* Practice Kubernetes scaling and self-healing
* Practice rolling updates and rollbacks
* Troubleshoot common Kubernetes failures
* Maintain the project using Git and GitHub
* Build practical CKA-level troubleshooting experience

## 🏗️ Project Architecture

```text
                    GitHub
                       │
                       │
                    Git
                       │
                       ▼
                Flask Notes API
                       │
                       ▼
                    Docker
                       │
                       ▼
                Kubernetes Cluster
                       │
                 ┌─────┴─────┐
                 │ Deployment │
                 └─────┬─────┘
                       │
                 ┌─────┴─────┐
                 │ ReplicaSet │
                 └─────┬─────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
             Pod      Pod      Pod
```

## 🚀 Application

The project contains a simple Flask REST API.

### Endpoints

| Endpoint  | Description                     |
| --------- | ------------------------------- |
| `/`       | Returns application information |
| `/health` | Health check endpoint           |
| `/notes`  | Returns sample notes            |

Example response from `/health`:

```json
{
  "status": "healthy"
}
```

## 📁 Project Structure

```text
k8s-mini-project/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── k8s/
│   └── # Kubernetes manifests will be added here
│
├── .gitignore
└── README.md
```

## 🐳 Docker

The Flask application is packaged into a Docker image.

The Dockerfile:

1. Uses Python 3.12
2. Creates `/app` as the working directory
3. Installs Flask
4. Copies the application
5. Exposes port `5000`
6. Starts the Flask application

## ☸️ Kubernetes Topics

The project will progressively cover the following concepts:

### Workloads

* Pod
* ReplicaSet
* Deployment
* Deployment strategies
* RollingUpdate
* Recreate

### Deployment Management

* Creating Deployments
* Scaling replicas
* Updating container images
* Rolling updates
* Rollout status
* Rollout history
* Rollbacks
* Revision history

### Reliability

* ReplicaSet self-healing
* Pod replacement
* Desired state
* Readiness and availability

### Troubleshooting

The project will intentionally introduce failures to practice troubleshooting:

* `ImagePullBackOff`
* `ErrImagePull`
* Failed rollouts
* Unready Pods
* Incorrect container images
* Deployment issues

## 🔄 Git Workflow

Git will be maintained throughout the project.

The workflow will be:

```text
Learn concept
     ↓
Implement
     ↓
Test
     ↓
Check git status
     ↓
Review git diff
     ↓
Commit
     ↓
Push to GitHub
```

Example commit:

```bash
git add .
git commit -m "feat: add Kubernetes deployment"
git push
```

## 🧪 Learning Approach

This project is being built incrementally rather than deploying everything at once.

Each Kubernetes concept will be:

1. Learned
2. Implemented
3. Tested
4. Troubleshot
5. Committed to Git

This makes the repository both a **learning environment** and a record of practical Kubernetes experience.

## 🛠️ Technologies

* Python
* Flask
* Docker
* Kubernetes
* kubectl
* Git
* GitHub
* kind

## 📌 Project Status

### Completed

* [x] Flask Notes API
* [x] Dockerfile
* [x] Python dependencies
* [x] Git repository
* [x] GitHub repository

### In Progress

* [ ] Kubernetes Namespace
* [ ] Kubernetes Deployment
* [ ] ReplicaSet management
* [ ] Pod scaling
* [ ] Kubernetes Service
* [ ] Self-healing testing
* [ ] Rolling updates
* [ ] Rollbacks
* [ ] Deployment troubleshooting

### Planned

* [ ] Resource requests and limits
* [ ] ConfigMaps
* [ ] Secrets
* [ ] Probes
* [ ] Persistent storage
* [ ] Ingress
* [ ] Monitoring
* [ ] Production-style deployment

## 🎓 CKA Practice

This project is designed to reinforce practical CKA skills including:

* Kubernetes resource management
* `kubectl` usage
* YAML manifests
* Deployments
* ReplicaSets
* Pods
* Services
* Scaling
* Rollouts
* Rollbacks
* Troubleshooting
* Cluster-level debugging

## 👨‍💻 Author

**Aditya Joshi**
