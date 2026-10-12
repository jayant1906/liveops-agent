# LiveOps Agent

LiveOps Agent is an incident-response project with a FastAPI backend, a React frontend, and a curated knowledge base for retrieval-backed diagnosis and remediation.

## Setup

Use a project virtual environment instead of the Homebrew-managed system Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

In VS Code, select the same interpreter:

```text
Cmd+Shift+P -> Python: Select Interpreter -> ./.venv/bin/python
```

If Pylance still shows missing imports, run `Pylance: Restart Language Server`.

## Environment

Create `backend/.env` with:

```bash
APP_NAME=LiveOps Agent
APP_ENV=development
API_PREFIX=/api
DATABASE_URL=postgresql+psycopg2:///liveops
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Run The Backend

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --app-dir backend
```

The API runs at `http://127.0.0.1:8000`.

## Run The Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at `http://127.0.0.1:5173`. It displays active incidents
and recent telemetry, refreshes automatically, and includes a failure-demo
button for testing the incident flow.

## Knowledge Base

The repository includes a small retrieval knowledge base:

- `knowledge_base/runbooks/`: operational runbooks
- `knowledge_base/architecture/`: system and dependency notes
- `knowledge_base/incidents/`: historical incidents with similar but not identical failures

To regenerate the JSONL chunks used by retrieval:

```bash
source .venv/bin/activate
python backend/scripts/ingest_documents.py
```

The ingestion pipeline is:

```text
load -> clean -> chunk -> metadata -> write
```

Output is written to:

```text
backend/data/knowledge_chunks.jsonl
```

You can override paths or chunk settings:

```bash
python backend/scripts/ingest_documents.py \
  --knowledge-base-path knowledge_base \
  --output-path backend/data/knowledge_chunks.jsonl \
  --chunk-size 50 \
  --chunk-overlap 5
```

## Vector Retrieval

Day 6 retrieval lives in:

- `backend/app/retrieval/embeddings.py`
- `backend/app/retrieval/vector_store.py`
- `backend/tests/test_vector_retrieval.py`

The retrieval flow is:

```text
documents -> embeddings -> FAISS index -> semantic search -> ranked metadata
```

Run the focused retrieval test from the project root:

```bash
.venv/bin/python -m unittest -v backend/tests/test_vector_retrieval.py
```

The test indexes four small fake documents, searches for:

```text
payment service database connection pool exhausted
```

and verifies that payment/database documents rank above unrelated authentication and cache documents. The printed score is FAISS L2 distance, so lower is more relevant.

## System Architecture

The backend is organized around an incident-response pipeline:

```text
Service request or failure injection
        ↓
Telemetry persisted to the database
        ↓
Threshold-based incident detection
        ↓
LangGraph investigation workflow
        ↓
Logs + metrics + deployments + dependencies
        ↓
BM25 + vector retrieval + CrossEncoder reranking
        ↓
Hypothesis scoring and diagnosis
        ↓
Recommended remediation
```

The current agent workflow is:

```text
Investigate
    ↓
Generate hypotheses
    ↓
Evaluate hypotheses
    ↓
Diagnosis
```

The agent does not execute remediation. It returns a recommendation with
`execute: false` so a human can review it first.

## Telemetry and Services

The simulated services are available under the `/api` prefix:

```text
GET /api/users/
GET /api/orders/
GET /api/payments/
```

Telemetry can be written and inspected through:

```text
GET  /api/telemetry/logs
POST /api/telemetry/logs
GET  /api/telemetry/metrics
POST /api/telemetry/metrics
GET  /api/telemetry/events
POST /api/telemetry/events
```

Posting a metric through `POST /api/telemetry/metrics` also runs threshold
detection automatically. Existing open incidents are deduplicated, so repeated
threshold breaches do not create duplicate alerts.

## Failure Injection

Available failure endpoints:

```text
POST /api/failures/database
POST /api/failures/slow-db
POST /api/failures/memory
POST /api/failures/dependency
POST /api/failures/deployment
```

The database failure endpoint is the complete Day 9 demonstration path. It
records a recent payment-service deployment, an error log, a 31% error rate,
100 database connections, and a failure event. It then detects incidents and
automatically starts the investigation workflow.

## Day 9 Demo

Start the backend:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --app-dir backend
```

Trigger the complete pipeline:

```bash
curl -X POST http://127.0.0.1:8000/api/failures/database
```

The response contains:

- created incidents;
- collected logs, metrics, deployments, dependencies, and historical incidents;
- BM25/vector/RAG results;
- reranked knowledge-base results;
- scored hypotheses;
- the final diagnosis;
- a recommended rollback that is not executed automatically.

The expected diagnosis is similar to:

```text
A database connection leak associated with the recent payment-service
deployment is the most likely cause.
```

The expected recommendation is similar to:

```json
{
  "action": "rollback_deployment",
  "service": "payment-service",
  "execute": false
}
```

The first request may take longer because the embedding model and CrossEncoder
model are initialized and the knowledge chunks are added to the vector index.

## Agent Tools

The agent tools are defined in `backend/app/agent/tools.py`:

- `get_logs()`
- `get_metrics()`
- `get_deployments()`
- `search_knowledge_base()`
- `search_historical_incidents()`
- `get_service_dependencies()`

The tools are exposed through `AGENT_TOOLS`, and the investigation graph is
created with:

```python
from app.agent.graph import run_investigation

result = run_investigation(incident, db, knowledge_searcher)
```

## Retrieval Evaluation

The hybrid search implementation supports these three modes:

```text
Vector only
BM25 + Vector
BM25 + Vector + CrossEncoder reranker
```

The knowledge-base searcher is initialized by
`backend/app/retrieval/knowledge_base.py`. It loads
`backend/data/knowledge_chunks.jsonl`, builds the FAISS index, and connects the
index to BM25 and the CrossEncoder reranker.

## Incident Detection

Detection currently checks the latest values for:

- error rate above `10.0`;
- latency above `1000.0 ms`;
- database connections above `90.0`.

Detection can also be run directly through:

```bash
curl -X POST http://127.0.0.1:8000/api/incidents/detect
```

## Project Structure

```text
backend/app/
├── agent/
│   ├── graph.py
│   ├── investigator.py
│   ├── diagnostician.py
│   ├── state.py
│   └── tools.py
├── detection/
├── failures/
├── retrieval/
│   ├── bm25.py
│   ├── embeddings.py
│   ├── hybrid_search.py
│   ├── knowledge_base.py
│   ├── reranker.py
│   └── vector_store.py
├── database/
├── services/
└── api/
```

## Verification

Run the focused vector retrieval test:

```bash
.venv/bin/python -m unittest -v backend/tests/test_vector_retrieval.py
```

Run syntax checks across the backend:

```bash
.venv/bin/python -m compileall -q backend/app
```

For a complete manual verification, run the backend and use the Day 9 demo
endpoint above. This requires the dependencies in `backend/requirements.txt`,
a working database configured through `DATABASE_URL`, and access to the
embedding and CrossEncoder model weights.
