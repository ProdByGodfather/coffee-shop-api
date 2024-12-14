from config.settings import app

from coffee.views import router as CoffeeRouter
from token_config.urls import router as TokenRouter


app.include_router(TokenRouter)
app.include_router(CoffeeRouter, prefix="/coffees", tags=['Coffee'])