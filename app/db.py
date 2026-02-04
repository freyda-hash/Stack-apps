from fastapi import FastAPI, HTTPException
import psycopg 

class database(DB_HOST:str, DB_NAME:str, DB_USER:str, DB_PASSWORD:str) -> None:

    def __init__(self):
        self.DB_HOST = DB_HOST
        self.DB_NAME= DB_NAME
        self.DB_USER = DB.USER
        self.DB_PASSWORD = DB.PASSWORD

    def db_dsn() -> str:
        return f"host={self.DB_HOST} port={self.DB_PORT} dbname={self.DB_NAME} user={self.DB_USER} password={self.DB_PASSWORD}"



