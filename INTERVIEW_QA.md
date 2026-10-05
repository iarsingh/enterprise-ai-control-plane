# enterprise-ai-control-plane — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does enterprise-ai-control-plane address, and what can you demonstrate?

A request is blocked until production is refused, cost is under the cap, a corpus citation is present, and the image tag is pinned. A complete request is `ready_for_readout`. `live` stays false.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/control/main.py`](src/control/main.py): Implementation or supporting configuration.
- [`src/control/review.py`](src/control/review.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/control/__init__.py`](src/control/__init__.py): Implementation or supporting configuration.
- [`tests/test_control.py`](tests/test_control.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `review` and explain the decision it makes?

The main walkthrough here is `review(request)` in [`src/control/review.py`](src/control/review.py#L1).

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

The implementation calls `image.endswith`, `missing.append`, `request.get`. In an interview, trace those calls in execution order using a fixture input.

## 4. Where would you add input-validation tests?

Start with the handlers `post_review` in [`src/control/main.py`](src/control/main.py#L7). Use the request schema or body access in each handler to build valid, missing-field, wrong-type, and boundary inputs. I would inspect existing tests before claiming coverage.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_control.py`](tests/test_control.py#L4) contains `test_blocks_prod_and_accepts_a_readout`:

```python
def test_blocks_prod_and_accepts_a_readout():
    client = TestClient(app)
    blocked = client.post("/review", json={"environment": "prod", "monthly_cost": 400, "cost_cap": 100, "citation": "", "image": "billing:latest"}).json()
    assert blocked["status"] == "blocked"
    assert blocked["live"] is False
    assert blocked["missing"] == ["policy", "cost_ok", "citation", "pinned_image"]
    ready = client.post("/review", json={"environment": "staging", "monthly_cost": 40, "cost_cap": 100, "citation": "corpus/refusals.md", "image": "billing:1.4.2"}).json()
    assert ready["status"] == "ready_for_readout"
    assert ready["live"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `POST /review` → `post_review` in [`src/control/main.py`](src/control/main.py#L7).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `review`?

In [`src/control/review.py`](src/control/review.py#L1), `review(request)` receives the inputs. The function computes these intermediate values:

- `missing = []`
- `image = request.get('image', '')`

Its result is defined by:

- `{'status': 'ready_for_readout', 'missing': [], 'live': False}`
- `{'status': 'blocked', 'missing': missing, 'live': False}`

## 12. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/control/review.py`](src/control/review.py#L1) branches on:

- `request.get('environment') == 'prod'`
- `request.get('monthly_cost', 0) > request.get('cost_cap', 0)`
- `not request.get('citation')`
- `':' not in image or image.endswith(':latest')`
- `missing`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
