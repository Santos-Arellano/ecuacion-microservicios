from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class Equation(BaseModel):
    a: float
    b: float
    c: float
    d: float

SUMA_URL = os.getenv("SUMA_URL", "http://suma:8000/sumar")
RESTA_URL = os.getenv("RESTA_URL", "http://resta:8000/restar")

@app.post("/ecuacion")
async def ecuacion(equation: Equation):
    async with httpx.AsyncClient() as client:
        # Call suma service (a + b)
        suma_response = await client.post(SUMA_URL, json={"a": equation.a, "b": equation.b})
        if suma_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error calling suma service")
        suma_result = suma_response.json()["result"]

        # Call resta service (c + d)
        resta_response = await client.post(RESTA_URL, json={"a": equation.c, "b": equation.d})
        if resta_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error calling resta service")
        resta_result = resta_response.json()["result"]

        # Compute final result: (a + b) - (c + d)
        result = suma_result - resta_result
        return {"a": equation.a, "b": equation.b, "c": equation.c, "d": equation.d, "result": result}