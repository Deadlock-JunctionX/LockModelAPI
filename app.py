from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import re
app = FastAPI()

model = None
pattern = r"\d+\s*[k]*['nghìn']*['ngàn']*['cành']*['triệu']*['trịu']*[tỉ]*[củ]*[trăm]*"

class Result(BaseModel):
    amount: List = list()
    intent: str = "NEUTRAL"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post('/process')
def detect_intent(ms: str):
    # intent = model(str)
    # raw_amount = re.findall(pattern, ms)
    raw_amount = ["30k", "3 củ"]
    amount = [norm_curency(a) for a in raw_amount]
    result = Result(
        amount=amount,
        intent="LEDING"
    )
    return JSONResponse(content=result,  media_type="application/json")



def norm_curency(raw_curency: str):
    raw_curency = re.sub(r"\s+","", raw_curency)
    raw_curency = re.sub(r"k","000", raw_curency)
    raw_curency = re.sub(r"cành","000", raw_curency)
    raw_curency = re.sub(r"ngàn","000", raw_curency)
    raw_curency = re.sub(r"nghìn","000", raw_curency)
    
    raw_curency = re.sub(r"trăm","00000", raw_curency)
    
    raw_curency = re.sub(r"củ","000000", raw_curency)
    raw_curency = re.sub(r"trịu","000000", raw_curency)
    raw_curency = re.sub(r"triệu","000000", raw_curency)

    raw_curency = re.sub(r"tỉ","000000000", raw_curency)

    return raw_curency