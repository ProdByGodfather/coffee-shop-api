from abarorm.fields import sqlite
from abarorm import SQLiteModel


from config.settings import db_conf


# SQLiteModel for Coffee
class Coffee(SQLiteModel):
    coffeeName = sqlite.CharField(max_length=200)
    coffeeType = sqlite.CharField(max_length=200)
    rate = sqlite.FloatField()
    commentCount = sqlite.IntegerField()
    image = sqlite.CharField(max_length=500)
    price = sqlite.FloatField()
    isLiked = sqlite.BooleanField()
    desc = sqlite.CharField()
    buyCount = sqlite.IntegerField()
    coffeeShopLocation = sqlite.CharField(max_length=1000)
    coffeeAddress = sqlite.CharField()

    class Meta:
        db_config = db_conf