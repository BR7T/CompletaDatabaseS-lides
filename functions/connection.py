from dotenv import load_dotenv
from mysql import connector
import os
load_dotenv()


def connection():
    try:
        conn = connector.connect(
            host= os.getenv("DB_HOST"),
            database= os.getenv("DB_DATABASE"),
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD")
        )
        return conn
    except connector.Error as err:
        print("ERRO: ",err)
        return None