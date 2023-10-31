from pydantic import BaseModel
from datetime import datetime,date,time

class User (BaseModel):
    username: str
    email: str
    height: float
    weight: float
    #need to take the birthdate with date() constructor, that will have as params the year,month and day
    birthdate: date

class Meal:
    meal_name: str
    quantity: float
    date: date
    time: time
    nutritional_info: dict
    user_id: int

    def __init__(self, name:str, quantity: float, date:date, time: time):
        self.meal_name=name
        self.quantity=quantity
        self.time=time
        self.date=date

    def set_nutritional_info(self, nutritional_info:dict):
       self.nutritional_info=nutritional_info