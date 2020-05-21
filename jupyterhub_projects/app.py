from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/home')
def home():
    return templates.TemplateResponse("home.html")