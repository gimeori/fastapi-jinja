from fastapi import APIRouter, status, Request
from src.models import *
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  login TEXT NOT NULL,
                  password TEXT NOT NULL,
                  name TEXT NOT NULL,
                  age INTEGER,
                  height INTEGER)''')
conn.commit()


app=APIRouter(prefix="/users", tags=["Users"])
templates=Jinja2Templates(directory="templates")


@app.post("/sign_up/", status_code=status.HTTP_201_CREATED)
async def sign_up(request: Request, user:UserSignUp):
    try:
        cursor.execute('''INSERT INTO Users (login, password, name, age, height)
                        VALUES (?, ?, ?, ?, ?)''', (user.login, user.password, user.name, user.age, user.height))
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message":f"Error: {e}"})
    

@app.post("/sign_in/", status_code=status.HTTP_200_OK)
async def sign_in(request: Request, user:UserSignIn):
    cursor.execute('''SELECT * FROM users WHERE login=? AND password=?''', (user.login, user.password))
    user = cursor.fetchone()
    if user:
        user_data = {
            "login": user[1],
            "name": user[3],
            "age": user[4],
            "height": user[5]
        }
        return templates.TemplateResponse("index.html", {"request": user_data})
    else:
        return JSONResponse(status_code=404, content={"message":"Пользователь не найден"})
    



@app.get("/base")
def get_base_page(request:Request):
    return templates.TemplateResponse("base.html",{"request": request})

@app.get("/index")
def get_idex_page(request:Request):
    return templates.TemplateResponse("index.html",{"request": request})