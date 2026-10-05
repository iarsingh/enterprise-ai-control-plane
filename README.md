# Enterprise AI Control Plane

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/control/main.py`](src/control/main.py) | HTTP handlers: `POST /review` |
| [`src/control/review.py`](src/control/review.py) | Functions: `review` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/control/__init__.py`](src/control/__init__.py) | Implementation or supporting configuration |
| [`tests/test_control.py`](tests/test_control.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn control.main:app --reload
```

<!-- project-guide:end -->

Level: 18 — Flagship capstone

Skills: Python, policy, cost, a citation, a pinned image

A request is blocked until production is refused, cost is under the cap, a corpus citation is present, and the image tag is pinned. A complete request is `ready_for_readout`. `live` stays false.

```bash
pip install -r requirements.txt
pytest -q
```
