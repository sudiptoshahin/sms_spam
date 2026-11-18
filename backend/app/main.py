from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import prediction, report


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/test')
def test():
    return {'message': 'Spam / Ham is now run!'}


# ---------- Attach router ------------
app.include_router(prediction.router)
app.include_router(report.router)
