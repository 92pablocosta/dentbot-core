# DentBot Core

DentBot Core is a ground-up modernization of the backend behind DentBot, an existing dental automation project. It is being developed publicly as a sanitized, testable, and better-structured replacement for the current backend. It currently focuses on the Python domain layer: a small, deterministic intent classifier with explicit business-rule priority and pytest coverage.

The existing DentBot remains operational independently while the new backend is developed and validated. Once DentBot Core is validated, the goal is to migrate existing DentBot workflows to it incrementally. The modernization emphasizes clear domain boundaries and deterministic behavior first, then incrementally adds automated tests, FastAPI, Docker, CI, and documented architectural decisions without coupling business rules to workflow tooling or an AI provider.

No real patient data, client credentials, private prompts, or production configuration from the original system are included in this repository.

## Current status

Implemented today:

- Python package using a `src/` layout
- Deterministic `classify_intent(message)` domain function
- Four supported outcomes: `appointment_request`, `emergency`, `pricing_question`, and `other`
- Explicit priority: emergency → pricing question → appointment request → fallback
- pytest suite with five tests
- Dependency and environment management with `uv`

Not implemented: FastAPI, n8n integration, Docker, CI, a database, external AI APIs, deployment, or real client integrations. These are planned engineering directions, not current capabilities.

## Architecture

### Current implementation

```text
Input message → Python keyword rules → structured intent string
```

The classifier normalizes the message and evaluates keyword groups in priority order. Keeping this logic deterministic makes the current behavior easy to inspect and test, especially where an emergency signal must take precedence over an appointment request.

### Planned workflow

```text
Test client → n8n webhook → DentBot Core / FastAPI → Python domain rules
            → structured decision → n8n routing → simulated response or log
```

This diagram is a target architecture, not a description of the current runtime. In the intended separation of responsibilities, n8n will handle orchestration and routing, FastAPI will expose the Python core over HTTP, and the domain layer will retain validation and deterministic business rules.

## Implemented behavior

The classifier recognizes Portuguese keyword signals for:

- emergencies, such as `urgente`, `emergência`, `sangramento`, and `inchaço`
- pricing questions, such as `preço`, `valor`, and `quanto custa`
- appointment requests, such as `marcar`, `consulta`, `horário`, and `disponível`

If more than one category appears, the implemented order decides the result. For example, a message requesting an appointment and mentioning urgency is classified as `emergency`. Messages without a recognized signal return `other`.

## Project structure

```text
src/dentbot_core/
  classifier.py       # deterministic intent rules
tests/
  test_classifier.py  # classifier behavior and priority tests
pyproject.toml        # project metadata and pytest configuration
uv.lock               # locked development dependencies
```

## Tech stack

- Python 3.14+
- `uv` for dependency management
- pytest for behavior verification

The project currently has no runtime dependencies. pytest is the only declared development dependency.

## Running locally

Install the locked project environment from the repository root:

```bash
uv sync
```

The project requires Python 3.14 or later, as declared in `pyproject.toml` and `uv.lock`.

## Running tests

```bash
uv run pytest -q
```

At this checkpoint, the suite contains five passing tests.

## Development roadmap

Planned next stages are deliberately outside the present implementation:

1. Add a FastAPI HTTP boundary around the domain core.
2. Connect that boundary to n8n webhook and routing workflows.
3. Add an optional AI-provider abstraction only where deterministic rules are insufficient.
4. Introduce Docker, CI, and deployment concerns in later stages.

## Design principles

- **Deterministic first:** business rules are explicit before introducing model-dependent behavior.
- **Testable boundaries:** the domain function is independent of HTTP, workflow tooling, and external services.
- **Incremental architecture:** integrations are planned as replaceable layers around a small core.
- **Scope discipline:** the repository demonstrates foundations and trade-offs rather than claiming production readiness.

## Disclaimer

DentBot Core is a public, sanitized backend replacement under active development and validation. It does not currently serve production traffic. The existing DentBot remains operational independently during this work. This repository contains no real patient data, clinic records, client credentials, private prompts, production configuration, or client integrations.
