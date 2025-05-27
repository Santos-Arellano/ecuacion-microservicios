from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    a: float
    b: float

@app.post("/restar")
async def restar(numbers: Numbers):
    result = numbers.a - numbers.b
    return {"result": result}