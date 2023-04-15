from fastapi import FastAPI

app = FastAPI()

model = None

@app.get("/health")
def health():
    return {"status":"ok"}


@app.post('/process')
def detect_intent(ms: str):
    label = model(str)
    if label == "LEDING":
        pass
    elif label == "PAYBACK":
        pass