from fastapi import FastAPI
from src.controllers.tracking import router as tracking_router

app = FastAPI()
app.include_router(tracking_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
