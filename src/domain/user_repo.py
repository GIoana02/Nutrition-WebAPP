from src.domain.user import User
from src.db.users import *
from datetime import date
from datetime import datetime

class UserRepository:
    def __init__(self, persistence):
        self.__persistence = persistence

    def write_user(self, user:User):
        return self.__persistence.write_user(user)

    def delete_user(self, username:str):
       return self.__persistence.delete_user(username)

    def get_user(self, username: str):
       return self.__persistence.get_user(username)

    def edit_user(self, username: str, email: str =None, height: float =None,weight:float = None, birthdate:date=None):
        return self.__persistence.edit_user(username, email, height, weight, birthdate)

    def list_users(self):
        return self.__persistence.list_users()
class MealRepository:
    def __init__(self, persistence):
        self.__persistence = persistence
    def insert_meal(self, username:str,meal:Meal):
        return self.__persistence.insert_meal(username, meal)

    def get_user_meals(self, username:str,start_date:date, end_date:date):
        return self.__persistence.get_user_meals(username, start_date, end_date)

    def delete_meal(self, username:str, meal_name:str):
        return self.__persistence.delete_meal(username,meal_name)

    def edit_user_meal(self, username: str, meal_name: str, meal: Meal):
        return self.__persistence.edit_user_meal(username,meal_name,meal)

    def get_meals_by_day(self, username:str,day:date):
        return self.__persistence.get_meals_by_day(username, day)

    def generate_calories_pie_chart(self, username, target_date :date):
        return self.__persistence.generate_calories_pie_chart(username,target_date)
#define a User object, with private fields
#accesed with property decorator
#user repo receives in constructor an object which knows how to save the users in a file or db
#in db folder create to classes one for file, one for db
#create a config.json in which we tell what type of persistence we have


#path="src/config.json"
#if os.path.exists(path) and os.stat(path).st_size != 0:
#    with open(path, "r") as jsonFile: