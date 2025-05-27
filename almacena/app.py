from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import mysql.connector
import os

app = FastAPI()

class Equation(BaseModel):
    a: float
    b: float
    c: float
    d: float

ECUACION_URL = os.getenv("ECUACION_URL", "http://ecuacion:8000/ecuacion")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT")),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )

@app.post("/almacena")
async def almacena(equation: Equation):
    async with httpx.AsyncClient() as client:
        # Call ecuacion service
        response = await client.post(ECUACION_URL, json=equation.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error calling ecuacion service")
        result = response.json()

    # Store in MySQL
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO resultados (a, b, c, d, resultado)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (result["a"], result["b"], result["c"], result["d"], result["result"]))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Data stored successfully", "result": result}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")