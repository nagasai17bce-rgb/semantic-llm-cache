# Semantic LLM Cache

## Overview

A prompt-cache layer that canonicalizes equivalent requests and provides TTL-based reuse before expensive model inference.

This repository is intentionally structured as a runnable reference implementation rather than a collection of notebooks. The service exposes a small HTTP contract, keeps the core domain logic isolated from the API layer, includes automated tests, and can be packaged as a container.

## Why this project exists

Modern AI systems are increasingly becoming distributed software systems rather than single prompts. They need explicit interfaces, policy boundaries, observability, failure handling, testing, and deployment paths. This project demonstrates those engineering concerns around a focused AI workload.

## Architecture

```
Client
  |
  v
FastAPI API
  |
  v
Domain Service
  |
  +--> Policy / validation
  +--> Domain logic
  +--> Provider or data adapters
  |
  v
Structured response
```

The current implementation keeps external infrastructure deliberately lightweight so the repository can run locally without proprietary credentials. Production deployments can replace the in-memory/demo components with managed infrastructure without changing the public API contract.

## Repository structure

```
app/
  __init__.py
  main.py       # HTTP API and request validation
  service.py    # Core domain behavior
tests/
  test_api.py   # API-level regression tests
examples/
  request.sh    # Runnable API example
Dockerfile       # Container image
pyproject.toml   # Python package and dependencies
.github/
  workflows/
    ci.yml       # Automated test pipeline
```

## Requirements

- Python 3.11+
- pip
- Docker (optional)
- curl or another HTTP client

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Health check:

```bash
curl http://localhost:8000/health
```

Run the project-specific example:

```bash
bash examples/request.sh
```

## API contract

### GET /health

Returns service health.

Example response:

```json
{"status":"ok"}
```

### POST /v1/run

Accepts a JSON request containing a `value` field.

```json
{"value":"demo request"}
```

The response is intentionally structured so callers can consume individual decisions, metadata, and intermediate results rather than parsing natural-language output.

## Testing

Run the complete test suite:

```bash
pytest -q
```

The tests exercise the HTTP contract and core behavior. In a production implementation, these should be complemented by integration tests against real infrastructure and contract tests for external providers.

## Docker

Build:

```bash
docker build -t semantic-llm-cache .
```

Run:

```bash
docker run --rm -p 8000:8000 semantic-llm-cache
```

## Engineering principles

1. **Deterministic boundaries** — business logic should be testable without an LLM.
2. **Explicit contracts** — API requests and responses use structured schemas.
3. **Approval before high-impact actions** — agents should not silently perform privileged operations.
4. **Observability by default** — production versions should emit traces, metrics, and audit events.
5. **Provider abstraction** — model and infrastructure dependencies should remain replaceable.
6. **Secure-by-default execution** — untrusted input should be validated before tools or infrastructure are reached.

## Production architecture

A production deployment would typically add:

- API gateway and authentication
- OAuth/OIDC or workload identity
- PostgreSQL for durable metadata
- Redis for caching and coordination
- Kafka/Pub/Sub for asynchronous work
- Object storage for large artifacts
- OpenTelemetry for distributed tracing
- Prometheus-compatible metrics
- Secrets manager/KMS
- Kubernetes or managed container runtime
- CI/CD with image scanning and deployment gates

## Reliability

Production hardening should include:

- Request timeouts
- Retries with exponential backoff
- Idempotency keys
- Circuit breakers
- Rate limiting
- Dead-letter queues
- Graceful shutdown
- Dependency health checks
- Structured logs
- SLOs and alerting

## Security

Do not place API keys or credentials in source code. Use environment variables locally and a managed secret store in production.

Recommended controls include:

- Authentication and authorization
- Tenant isolation
- Input validation
- Output validation
- Audit logging
- PII/secret redaction
- Least-privilege service identities
- Network egress controls
- Dependency and container scanning

## CI/CD

GitHub Actions runs the test suite on pushes and pull requests. A production pipeline should extend this with:

1. Formatting/linting
2. Unit tests
3. Integration tests
4. Security scanning
5. Container build
6. Container vulnerability scan
7. Artifact signing
8. Staging deployment
9. Smoke tests
10. Production approval/deployment

## Roadmap

- Replace demo state with durable infrastructure
- Add authentication and multi-tenancy
- Add OpenTelemetry traces
- Add provider adapters
- Add load and failure testing
- Add infrastructure-as-code
- Add Kubernetes deployment manifests
- Add production dashboards and SLOs

## Status

This repository is a runnable engineering reference. The local implementation intentionally avoids requiring paid external services, while the architecture documents the path to a production deployment.

## Project-specific design notes

### Core problem
A prompt-cache layer that canonicalizes equivalent requests and provides TTL-based reuse before expensive model inference.

### Recommended production components
- Stateless API service for request validation and orchestration
- Durable state where workflow history or user data must survive restarts
- Queue/worker separation for long-running operations
- Model/provider adapters behind stable interfaces
- Centralized policy and authorization checks
- Metrics and traces around every external dependency

### Key design trade-off
The repository favors a small deterministic local implementation over hidden cloud dependencies. This makes the code easy to run, review, test, and extend while keeping the architectural boundary visible.

### What to replace for production
The in-memory/demo behavior should be replaced with managed storage and real provider integrations appropriate to the deployment environment. Preserve the domain service interface so the API and tests remain stable during that migration.
