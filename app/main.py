from tempfile import NamedTemporaryFile
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

import app.labs as labs


app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/public', StaticFiles(directory='app/public'), name='public')

@app.get('/')
def root():
    return RedirectResponse(url="/public/index.html")


@app.get('/files/physics/1_2.xlsx')
def physics_1_2():
    workbook = labs.physics_1_2.create_workbook()
    tmp = NamedTemporaryFile(delete=False)
    workbook.save(tmp.name)
    return FileResponse(tmp.name, filename='Лабораторна 1-2.xlsx')
