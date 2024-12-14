from abarorm.fields import sqlite
from abarorm import SQLiteModel

from config.settings import db_conf


class User(SQLiteModel):
    username = sqlite.CharField(unique=True, max_length=200)
    password = sqlite.CharField(max_length=500)
    first_name = sqlite.CharField(max_length=100)
    last_name = sqlite.CharField(max_length=100)
    
    class Meta:
        db_config = db_conf
    
