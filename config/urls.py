from config.settings import app

from coffee.views import router as CoffeeRouter


app.include_router(CoffeeRouter, prefix="/coffees", tags=['Coffee'])