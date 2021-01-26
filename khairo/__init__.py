from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from mongoengine import connect, disconnect
from fastapi.staticfiles import StaticFiles
from khairo.settings import DEBUG
from khairo.backend.view import accountView

# template = Jinja2Templates(directory="./khairo/front/public").TemplateResponse

app = FastAPI(debug=DEBUG)
# from khairo.frontend.views import homeView

# app.mount("/static", StaticFiles(directory="./khairo/front"), name="static")
app.include_router(accountView.router)

@app.on_event("startup")
def connectDatabase():
    if  connect(db="khairo_diet", alias="core"):
        print("database connected")



@app.on_event("shutdown")
def disconnectDatabase():
    if disconnect(alias="core"):
        print("database disconnected")
