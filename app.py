from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from primes import primes
from train_stations import trains

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve the HTML file
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", context=dict(request=request))


app.include_router(primes.router)
app.include_router(trains.router)