from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    a: float
    b: float

@app.post("/sumar")
async def sumar(numbers: Numbers):
    result = numbers.a + numbers.b
    return {"result": result}