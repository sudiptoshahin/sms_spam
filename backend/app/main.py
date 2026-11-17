from fastapi import FastAPI, Response, status, HTTPException
from app import models
from app.database import engine, Base
from app.routers import prediction


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/test')
def test():
    return {'message': 'Spam / Ham is now run!'}


# ---------- Attach router ------------
app.include_router(prediction.router)