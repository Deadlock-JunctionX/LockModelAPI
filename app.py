import re
from http.client import HTTPException
from typing import List

import torch
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from handler import IntentionDetector

app = FastAPI()
intent_detector = IntentionDetector()
pattern = r"\d+\s*[k]*['nghìn']*['ngàn']*['cành']*['triệu']*['trịu']*[tỉ]*[củ]*[trăm]*"


class Result(BaseModel):
    amount: List = list()
    intent: str = "NEUTRAL"


@app.on_event("startup")
def on_start():
    torch.set_num_threads(1)
    intent_detector.load()


@app.get("/ping")
def ping():
    if intent_detector.ready == False:
        raise HTTPException(detail="Service not ready :<", status_code=503)
    return {"ping": "pong"}


def regex_money(ms: str) -> List[str]:
    raw_amounts = re.findall(pattern=pattern, string=ms)
    amounts = [norm_curency(a) for a in raw_amounts]
    return amounts


@app.post("/process")
def detect_intent(ms: str):
    intent = intent_detector.predict(ms)
    result = Result(amount=regex_money(ms), intent=intent)

    return JSONResponse(content=result.__dict__, media_type="application/json")


def norm_curency(raw_curency: str):
    raw_curency = re.sub(r"\s+", "", raw_curency)
    raw_curency = re.sub(r"k", "000", raw_curency)
    raw_curency = re.sub(r"cành", "000", raw_curency)
    raw_curency = re.sub(r"ngàn", "000", raw_curency)
    raw_curency = re.sub(r"nghìn", "000", raw_curency)

    raw_curency = re.sub(r"trăm", "00000", raw_curency)

    raw_curency = re.sub(r"củ", "000000", raw_curency)
    raw_curency = re.sub(r"trịu", "000000", raw_curency)
    raw_curency = re.sub(r"triệu", "000000", raw_curency)

    raw_curency = re.sub(r"tỉ", "000000000", raw_curency)
    raw_curency = re.sub(r"[^0-9]", "", raw_curency)

    return int(raw_curency)
