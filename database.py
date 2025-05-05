import mysql.connector

DATABASE_CONFIG = {
    "host":"127.0.0.1",
    "user":"root",
    "password":"Sql@9667244829",
    "database":"tapcart"
}

## Create the connection with the Database

def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)