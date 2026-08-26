from fastapi import FastAPI
from pydantic import BaseModel

class Sum(BaseModel):
    num1: int
    num2: int

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World22!"}

@app.post("/calculate/{item_id}")
async def sum(item_id: int, sum1: Sum):
    return {item_id: sum1.num1 + sum1.num2}
