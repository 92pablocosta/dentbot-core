# DentBot Core

DentBot Core is a public, sanitized modernization of the backend behind DentBot, a dental automation project. It provides a small Python domain layer for classifying incoming messages and turning those classifications into explicit, testable decisions.

The existing DentBot remains operational independently while this replacement is developed and validated. No patient data, clinic records, credentials, private prompts, production configuration, or live client integrations are included here.

## Current status

Implemented:

- A deterministic Portuguese-language intent classifier
- Structured domain decisions for each supported intent
- A minimal FastAPI application with a `POST /decisions` endpoint
- pytest coverage for the classifier, decision mapping, and endpoint availability
- Dependency management with `uv`

The HTTP endpoint is deliberately only a placeholder at this stage: it accepts requests and returns `{}`, but does **not** yet call the decision layer or validate a message payload.

Not implemented: HTTP request/response schemas, wiring between the API and the domain decision function, n8n integration, Docker, CI, persistence, external AI providers, deployment, and real client integrations.

## Architecture

```text
Message
  │
  ▼
classify_intent(message) ──► intent string
  │
  ▼
make_decision(message) ────► Decision(intent, action, message)

FastAPI app
  └── POST /decisions ─────► {}   (placeholder; not yet connected to the domain layer)
```

The domain code is independent of FastAPI and other integrations. This keeps business behavior deterministic and directly testable while HTTP and workflow concerns evolve around it.

## Supported intents and decisions

The classifier normalizes a message with `strip().lower()` and checks categories in this priority order:

| Priority | Intent | Example signals | Decision action |
| --- | --- | --- | --- |
| 1 | `emergency` | `urgente`, `emergência`, `sangramento`, `inchaço` | `emergency_triage` |
| 2 | `pricing_question` | `preço`, `valor`, `quanto custa` | `pricing_response` |
| 3 | `appointment_request` | `marcar`, `consulta`, `horário`, `disponível` | `appointment_intake` |
| 4 | `other` | no recognized signal | `human_handoff` |

For messages with signals from multiple categories, the highest-priority category wins. For example, `Quero marcar uma consulta urgente` is classified as `emergency`.

`make_decision(message)` returns a dataclass value with these fields:

```python
Decision(
    intent="pricing_question",
    action="pricing_response",
    message="A consulta custa R$ 250. Os demais serviços são avaliados durante a consulta.",
)
```

## Project structure

```text
src/dentbot_core/
  api.py              # FastAPI application and placeholder endpoint
  classifier.py       # deterministic intent rules
  decision.py         # intent-to-decision mapping
tests/
  test_api.py         # endpoint availability
  test_classifier.py  # classification and priority behavior
  test_decision.py    # structured decision behavior
pyproject.toml        # project metadata and test configuration
uv.lock               # locked dependencies
```

## Requirements

- Python 3.14 or later
- [`uv`](https://docs.astral.sh/uv/)

## Setup and tests

From the repository root, install the locked environment:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest -q
```

## Domain usage

```python
from dentbot_core.decision import make_decision

decision = make_decision("Quero marcar uma consulta urgente")

assert decision.intent == "emergency"
assert decision.action == "emergency_triage"
```

## Roadmap

1. Define request and response schemas for the API.
2. Connect `POST /decisions` to `make_decision`.
3. Integrate the HTTP boundary with n8n workflows.
4. Add optional AI-provider abstractions only where deterministic rules are insufficient.
5. Introduce Docker, CI, deployment, and persistence as later infrastructure layers.

## Design principles

- **Deterministic first:** business rules remain explicit before model-dependent behavior is introduced.
- **Testable boundaries:** the domain layer does not depend on HTTP, workflow tooling, or external services.
- **Incremental architecture:** integrations are replaceable layers around a small core.
- **Scope discipline:** the repository documents current capabilities without presenting it as production-ready.
