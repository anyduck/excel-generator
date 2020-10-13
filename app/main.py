from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.labs import physics_1_2


app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/public', StaticFiles(directory='public'), name='public')
app.include_router(physics_1_2.router)

@app.get('/')
def root():
    return RedirectResponse(url="/public/index.html")



