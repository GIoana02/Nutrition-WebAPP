from fastapi import APIRouter
from src.domain.user import User
from src.db.users import UserFile
from src.db.users import UserDB
from src.domain.user_repo import UserRepository
from src.domain.user_repo import MealRepository
import os
import json
from datetime import datetime, date, time
from src.domain.user import Meal
import requests
import logging

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

meals_repo=UserRepository(persistence_obj)

meal_router=APIRouter(tags=["Meals"])
def get_nutrition(name: str, quantity: float,date:date, time: time):

    meal=Meal(name,quantity,date,time)
    query=f"{quantity/10}g {name}"
    api_url = "https://api.api-ninjas.com/v1/nutrition"

    response = requests.get(api_url, params={"query": query},
                            headers={'X-Api-Key': '9T8k9Zcl5c6dD69z2Xx+lA==zEoawa49fNwGkKyD'})

    print(response)
    meal.set_nutritional_info(response.content)
    return meal

@meal_router.post("/{username}/meal/{meal_name}")
async def insert_meal(username: str, meal_name:str, quantity:float, date: date, time:time):
    meal=get_nutrition(meal_name,quantity,date,time)
    return meals_repo.insert_meal(username,meal)

@meal_router.get("/{username}/meals")
async def get_user_meals(username:str, start_date: date, end_date: date):
    return meals_repo.get_user_meals(username, start_date, end_date)

@meal_router.delete("/{username}/delete-meal/{meal_name}")
async def delete_meal(username:str, meal_name:str):
    return meals_repo.delete_meal(username,meal_name)
@meal_router.put("/{username}/edit-meal/{meal_name}")
async def edit_user_meal(username: str, meal_name: str, new_meal_name: str  , new_quantity: float ,date:date, time: time):
    meal=get_nutrition(new_meal_name,new_quantity,date,time)
    return meals_repo.edit_user_meal(username,meal_name,meal)

@meal_router.get("/{username}/list-meals/day/{day}")
async def get_meals_by_day(username:str, day:date):
    return meals_repo.get_meals_by_day(username,day)