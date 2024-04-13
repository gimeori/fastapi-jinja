from fastapi import FastAPI
from src.users import app as router_users


app=FastAPI()
app.include_router(router_users)

