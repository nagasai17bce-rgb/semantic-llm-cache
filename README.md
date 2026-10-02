# Semantic LLM Cache

## Overview
A prompt-cache layer that canonicalizes equivalent requests and provides TTL-based reuse before expensive model inference.

This repository is a runnable reference implementation with a clean API/domain boundary. It intentionally avoids mandatory cloud credentials so engineers can clone it, run it locally, inspect the behavior, and replace demo components incrementally.

## Architecture
```
Client -> FastAPI -> Domain Service -> Policy / State / Provider adapters -> JSON response
```

## Repository structure
- `app/main.py` — HTTP interface and validation
- `app/service.py` — core domain logic
- `tests/test_api.py` — regression tests
- `examples/request.sh` — end-to-end local example
- `Dockerfile` — production-style container entrypoint
- `.github/workflows/ci.yml` — CI
- `pyproject.toml` — package metadata

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Then:
```bash
curl http://localhost:8000/health
bash examples/request.sh
pytest -q
```

## API
`GET /health` returns service health.

`POST /v1/run` accepts:
```json
{"value":"demo request"}
```

The API returns structured JSON to make downstream automation reliable.

## Local vs production
The local implementation is deliberately deterministic. Production should replace in-memory behavior with appropriate managed systems while retaining the same domain contract.

## Reliability
Use request deadlines, retries/backoff, circuit breakers, rate limiting, idempotency, graceful shutdown, dead-letter handling, dependency health checks, and SLO-based alerting.

## Security
Use OIDC/workload identity, least privilege, tenant isolation, secret management, input/output validation, audit logs, PII/secret redaction, dependency scanning, and restricted network egress.

## Observability
Instrument requests and provider calls with OpenTelemetry traces and metrics for latency, errors, throughput, cache/provider decisions, and cost.

## Testing
The repository includes API regression tests. Extend them with integration tests, property tests, load tests, provider contract tests, and failure injection.

## Deployment
Build with:
```bash
docker build -t semantic-llm-cache .
```
Run with:
```bash
docker run --rm -p 8000:8000 semantic-llm-cache
```

For production, use a managed container platform or Kubernetes with secrets, health probes, autoscaling, and centralized logs.

## Engineering trade-offs
The project favors transparent, testable control flow over hiding behavior inside prompts. Model calls, storage, queues, and external systems should be adapters rather than hard-coded dependencies.

## Roadmap
- Durable state and distributed coordination
- Authentication and multi-tenancy
- Real provider integrations
- OpenTelemetry dashboards
- Load/failure testing
- Infrastructure as code
- Production deployment manifests

## Project-specific design
**Core problem:** A prompt-cache layer that canonicalizes equivalent requests and provides TTL-based reuse before expensive model inference.

**Production path:** introduce real infrastructure behind stable interfaces, preserve structured responses, and add policy/observability at every external boundary.