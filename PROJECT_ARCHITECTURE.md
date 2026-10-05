# enterprise-ai-control-plane — project architecture

[README](README.md) · [Interview questions and answers](INTERVIEW_QA.md)

## Purpose and scope

A request is blocked until production is refused, cost is under the cap, a corpus citation is present, and the image tag is pinned. A complete request is `ready_for_readout`. `live` stays false.

This document describes files and symbols in this checkout. Deployment templates and statements in the original overview are distinguished from a verified running environment.

## Component diagram

```mermaid
flowchart LR
    M0["src/control/__init__.py"]
    M1["src/control/main.py"]
    M2["src/control/review.py"]
    M1 -->|imports| M2
```

For Python repositories, arrows show resolved local imports, not network calls or deployment order. Otherwise the diagram is a repository component map; containment arrows do not assert runtime integration.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| [`src/control/main.py`](src/control/main.py) | HTTP handlers: `POST /review` |
| [`src/control/review.py`](src/control/review.py) | Functions: `review` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/control/__init__.py`](src/control/__init__.py) | Implementation or supporting configuration |
| [`tests/test_control.py`](tests/test_control.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

## Request interface

| Method and path | Handler | Source |
| --- | --- | --- |
| `POST /review` | `post_review` | [`src/control/main.py`](src/control/main.py#L7) |

The table lists literal route decorators found in the inspected Python modules. Router prefixes and middleware can add behavior; check the linked handler and application setup before calling an endpoint.

## Implementation walkthrough

### `review(request)`

Source: [`src/control/review.py`](src/control/review.py#L1).

Calls visible in this function: `image.endswith`, `missing.append`, `request.get`.

```python
def review(request):
    missing = []
    if request.get("environment") == "prod":
        missing.append("policy")
    if request.get("monthly_cost", 0) > request.get("cost_cap", 0):
        missing.append("cost_ok")
    if not request.get("citation"):
        missing.append("citation")
    image = request.get("image", "")
    if ":" not in image or image.endswith(":latest"):
        missing.append("pinned_image")
    if missing:
        return {"status": "blocked", "missing": missing, "live": False}
    return {"status": "ready_for_readout", "missing": [], "live": False}
```

## Data flow and design decisions

### What is the input-to-output contract of `review`

In [`src/control/review.py`](src/control/review.py#L1), `review(request)` receives the inputs. The function computes these intermediate values:

- `missing = []`
- `image = request.get('image', '')`

Its result is defined by:

- `{'status': 'ready_for_readout', 'missing': [], 'live': False}`
- `{'status': 'blocked', 'missing': missing, 'live': False}`

### Which decision rules or boundary conditions should an interviewer challenge

The implementation in [`src/control/review.py`](src/control/review.py#L1) branches on:

- `request.get('environment') == 'prod'`
- `request.get('monthly_cost', 0) > request.get('cost_cap', 0)`
- `not request.get('citation')`
- `':' not in image or image.endswith(':latest')`
- `missing`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.

## Setup and verification

The following commands are derived from the checked-in dependency/test contracts. Execute them from the repository root; the block prepares a local environment, not a cloud deployment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Python dependencies: [`requirements.txt`](requirements.txt).

Test entry points: [`tests/test_control.py`](tests/test_control.py).

Automation definitions: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Read their triggers and job steps to determine what CI actually runs.

## Operating boundaries and design review

Before turning this checkout into a customer deployment, establish the input contract, data ownership, access controls, failure response, evaluation criteria, and rollback owner. Repository fixtures and unit tests demonstrate local behavior; they do not establish throughput, uptime, compliance, or business impact.

A useful architecture review starts with the linked implementation: identify where input enters, where a decision is made, which state can change, and which external dependency can fail. Add a deployment view only for infrastructure that is actually configured and exercised.
