from abarorm import SQLiteModel
from abarorm.fields import sqlite

from config.db import db_conf
from account.models import User
from coffee.models import Coffee


class Cart(SQLiteModel):
    user = sqlite.ForeignKey(User, on_delete='CASCADE')
    coffee = sqlite.ForeignKey(Coffee, on_delete='CASCADE')
    count = sqlite.IntegerField()
    
    class Meta:
        db_config = db_conf
    