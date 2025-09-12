# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Form, Depends
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from model import Model
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')
model = Model()

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get("/any_answer")
async def any_answer(promt: str, link: str):
    result = model.get_any_answer(promt, link)
    return {"answer": result}

@app.get("/what_answer")
async def what_answer(link: str):
    result = model.get_what_answer(link)
    return {"answer": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
