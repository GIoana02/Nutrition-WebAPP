from fastapi import APIRouter
from src.domain.user import User
from src.db.users import UserFile
from src.db.users import UserDB
from src.domain.user_repo import UserRepository
import os
import json
from datetime import date
import logging

user_router=APIRouter(tags=["Users"])

def read_persistence():
    path="src/config.json"
    if os.path.exists(path) and os.stat(path).st_size != 0:
        with open(path, "r") as jsonFile:
            persistence=json.load(jsonFile)
            return persistence.get("persistence")

persistence=read_persistence()

if persistence=="json":
        persistence_obj = UserFile()

elif persistence=="sql":
        persistence_obj= UserDB()

user_repo=UserRepository(persistence_obj)
@user_router.post("/{username}/add")
async def add_user(username:str, email:str, height:float,weight:float, birthdate: date):
    user=User
    user.username=username
    user.email=email
    user.height=height
    user.weight=weight
    user.birthdate=birthdate
    return user_repo.write_user(user)

@user_router.get("/{username}/user-info")
async def get_user(username: str):
    return user_repo.get_user(username)

@user_router.delete("/{username}/delete-user")
async def delete_user(username: str):
   return user_repo.delete_user(username)

@user_router.put("/{username}/edit-info")
async def edit_user(username: str, email:str =None, height:float =None,weight:float = None,birthdate:date =None):
    return user_repo.edit_user(username, email, height, weight, birthdate)

@user_router.get("/users/list")
async def list_users():
    logging.info("ERROR")
    return user_repo.list_users()

