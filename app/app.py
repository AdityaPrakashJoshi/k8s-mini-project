from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Notes API",
        "version": "v1"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/notes")
def notes():
    return jsonify([
        {
            "id": 1,
            "title": "Learn Kubernetes",
            "content": "Deployments and ReplicaSets"
        },
        {
            "id": 2,
            "title": "Practice CKA",
            "content": "Troubleshooting Pods"
        }
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)