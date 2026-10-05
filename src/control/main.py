from control.ops import router as ops_router
from fastapi import FastAPI
from control.review import review

app = FastAPI()
app.include_router(ops_router, prefix="/v1")

@app.post("/review")
def post_review(body: dict):
    return review(body)
