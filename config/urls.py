from config.settings import app

from coffee.views import router as CoffeeRouter
from token_config.urls import router as TokenRouter
from account.views import router as UserRouter
from cart.views import router as CartRouter


app.include_router(TokenRouter)
app.include_router(UserRouter, prefix="/account", tags=['Account'])
app.include_router(CoffeeRouter, prefix="/coffees", tags=['Coffee'])
app.include_router(CartRouter, prefix="/cart", tags=['cart'])