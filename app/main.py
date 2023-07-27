from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

# from random import randrange
import psycopg2

# from psycopg2.extras import RealDictCursor


# Internal import
from database import engine, Base
from routers import user, event, auth

Base.metadata.create_all(bind=engine)


app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(database='fastapi', user='kufre', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("error: %s" % error)
#         time.sleep(2)

app.include_router(user.router)
app.include_router(event.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    context = {"name": "samuel", "age": 27, "sex": "male", "favorite": True}
    return context


# CREATE TABLE Events (id serial PRIMARY KEY, name varchar (50) NOT NULL, content text NOT NULL, published bool NOT NULL, rating INT);

#  name: str
#     host: str
#     description: str
#     venue: str
#     attendee: int
#     date: str
#     time: str
