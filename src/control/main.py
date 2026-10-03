from fastapi import FastAPI
from control.review import review

app = FastAPI()

@app.post("/review")
def post_review(body: dict):
    return review(body)
