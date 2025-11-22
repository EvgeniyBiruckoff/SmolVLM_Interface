# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Form, Depends
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from model import Model
from urllib.parse import unquote
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')
model = Model()

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get("/any_answer")
async def any_answer(prompt: str):
    result = model.get_any_answer(prompt)
    return {"answer": result}

@app.get("/what_answer")
async def what_answer():
    result = model.get_what_answer()
    return {"answer": result}

@app.get("/set_image")
async def set_image(link: str):
    result = model.set_image(link)
    return {}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
