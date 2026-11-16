from fastapi import FastAPI, Response, status, HTTPException

app = FastAPI()


@app.get('/test')
def test():
    return {'message': 'Spam / Ham is now run!'}