# AstroML

## Dynamic Graph Machine Learning Framework for the Stellar Network

**AstroML** is a research-driven Python framework for building **dynamic graph machine learning models** on the Stellar Development Foundation Stellar blockchain.

It treats blockchain data as a **multi-asset, time-evolving graph**, enabling advanced ML research on transaction networks such as fraud detection, anomaly detection, and behavioral modeling.

---

## ✨ Features

AstroML provides end-to-end tooling for:

* Ledger ingestion and normalization
* Dynamic transaction graph construction
* Feature engineering for blockchain accounts
* Graph Neural Networks (GNNs)
* Self-supervised node embeddings
* Anomaly detection
* Temporal modeling
* Reproducible ML experimentation
* Autonomous LLM agents for multi-step reasoning and task execution

---

## 🧠 Core Idea

Blockchain networks are naturally **graph-structured systems**:

| Blockchain Concept | Graph Representation |
| ------------------ | -------------------- |
| Accounts           | Nodes                |
| Transactions       | Directed edges       |
| Assets             | Edge types           |
| Time               | Dynamic dimension    |

Most analytics tools rely on static heuristics or SQL queries.

**AstroML instead enables:**

* Dynamic graph learning
* Temporal GNNs
* Representation learning
* Research-grade experimentation

---

## 🎯 Target Users

AstroML is designed for:

* ML researchers
* Graph ML engineers
* Fraud detection teams
* Blockchain data scientists

---

## 🏗 Architecture Overview

```
Ledger → Ingestion → Normalization → Graph Builder → Features → GNN/ML Models → Experiments
```


## 🚀 Getting Started

### Using Docker (Recommended)

For the quickest setup with all dependencies, use Docker:

```bash
# Clone and navigate to repository
git clone https://github.com/Traqora/astroml.git
cd astroml

# Start with Docker
cp .env.example .env
./scripts/docker-start.sh core

# Access services
curl http://localhost:8000            # API
open http://localhost:3000            # Grafana
```

📚 **Full Docker Setup**: See [DOCKER.md](./DOCKER.md) for comprehensive documentation including:
- [Docker Quick Reference](./DOCKER_QUICK_REFERENCE.md) - Quick commands and common tasks
- [Environment Configuration](./docker-env-guide.md) - Configuration guide
- [Production Deployment](./DOCKER_PRODUCTION_DEPLOYMENT.md) - Production setup
- [Troubleshooting](./DOCKER_TROUBLESHOOTING.md) - Common issues and solutions

### Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/Traqora/astroml.git
cd astroml
```

### 2. Create environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure database

Create a PostgreSQL database and update:

```
config/database.yaml
```

---

## 🤖 LLM Agent Framework

AstroML includes an LLM agent framework for **multi-step reasoning and autonomous task execution** over the graph pipeline. It is provider agnostic, dependency light (the core loop is standard library only) and traces every step so runs stay auditable.

```bash
# Offline smoke test with the deterministic echo provider
python -m astroml.agent "Summarise this transaction graph"

# Against a local Ollama server, with task decomposition
python -m astroml.agent --provider ollama --model llama3.1 --plan \
  "Rank the busiest accounts and flag anything unusual"

# Analyse a graph file and print the full trace as JSON
python -m astroml.agent --edges data/edges.json --json "How many accounts?"
```

```python
from astroml.agent import (
    AgentConfig,
    AgentExecutor,
    build_default_registry,
    provider_from_env,
)

agent = AgentExecutor(
    llm=provider_from_env(),           # echo | scripted | openai | ollama | ...
    tools=build_default_registry(),    # graph_overview, window_stats, ...
    config=AgentConfig(mode="auto", max_steps=8),
)
result = agent.run("Which accounts look unusual?")

print(result.answer)
print(result.trace.summary())
```

📚 **Full guide**: [docs/agent-framework.md](./docs/agent-framework.md) — providers, tools, memory, planning, CLI flags and design notes.

---

## 📥 Data Ingestion

Backfill ledgers:

```bash
python -m astroml.ingestion.backfill \
  --start-ledger 1000000 \
  --end-ledger 1100000
```

---

## 🕸 Build Graph Snapshot

Create a rolling time window graph:

```bash
python -m astroml.graph.build_snapshot --window 30d
```

---


## 🧪 Synthetic Fraud Pattern Injection

Create benchmark datasets by injecting controlled fraud structures into a clean ledger copy:

```bash
python -m astroml.ingestion.synthetic_fraud_injector \
  --input data/clean_ledger.jsonl \
  --output data/ledger_with_fraud.jsonl \
  --summary outputs/fraud_injection_summary.json \
  --sybil-clusters 3 \
  --sybil-cluster-size 8 \
  --wash-loops 2 \
  --wash-loop-size 5
```

The injector appends transactions tagged with `synthetic_fraud=true` and `fraud_pattern` (`sybil_cluster` or `wash_trading_loop`) for downstream benchmarking.

---
## 🤖 Train Baseline GCN

```bash
python -m astroml.training.train_gcn
```

---

## 📊 Example Use Cases

* [Liquidity Monitoring for the Stellar Community Fund](docs/scf-liquidity-monitoring.md)
* Fraud / scam detection
* Account clustering
* Transaction risk scoring
* Temporal behavior modeling
* Self-supervised embeddings
* Network anomaly detection

---

## 🔬 Research Goals

AstroML emphasizes:

* Reproducibility
* Modular experimentation
* Scalable ingestion
* Temporal graph learning
* Production-ready ML pipelines

---

## 🛠 Tech Stack

* Python
* PyTorch / PyTorch Geometric
* PostgreSQL
* NetworkX / graph tooling

---

## 📌 Roadmap

* [ ] Real-time streaming ingestion
* [ ] Temporal GNN models
* [ ] Contrastive learning pipelines
* [ ] Feature store
* [ ] Model benchmarking suite
* [ ] Docker deployment

---

## 🤝 Contributing

Contributions are welcome!

```bash
fork → branch → commit → PR
```

Please open issues for bugs or feature requests.

---

## 📜 License

MIT License


