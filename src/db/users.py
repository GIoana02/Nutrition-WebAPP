import json
import os.path
import sqlite3
from src.domain.user import User
from datetime import date, datetime, timedelta, time
from src.domain.user import Meal
#import plotly.express as px

class UserDB:

    user_id:int

    def __init__(self):
        self.database_name="src/my_database.db"
        self.table_name="users"
        self.meal_table = "meals"

    def create_table(self):
        # Connect to the DB
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()

        # Create table users
        command=f"CREATE TABLE IF NOT EXISTS {self.table_name}(username, email, height, weight, birthdate)"
        cur.execute(command)
        con.commit()
        con.close()

    def create_meal_table(self):
         # Connect to the DB
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()

        # Create table users
        command = f"CREATE TABLE IF NOT EXISTS {self.meal_table} (username, meal_date, meal_time, meal, quantity, nutritional_info)"
        cur.execute(command)
        con.commit()
        con.close()

    def connect_database(self):
        con=sqlite3.connect(self.database_name)
        cur=con.cursor()
        return con, cur

    def write_user(self, user: User):
        self.create_table()
        connection, cursor=self.connect_database()

        cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = ? OR email = ?", (user.username, user.email))
        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            return "User already used or this email is already registered"

        cursor.executemany(f"INSERT INTO {self.table_name} VALUES(?, ?, ?, ?, ?)", [(user.username, user.email, user.height, user.weight, user.birthdate)] )


        connection.commit()
        connection.close()
        return (f"User {user.username} added successfully!")

    def get_user(self, user_name: str):
        con, cur = self.connect_database()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE username = ?", (user_name,))
        user_data=cur.fetchone()
        con.close()
        return (f"User: {user_data}")

    def delete_user(self, user_name:str):
        con, cur = self.connect_database()
        command = f"DELETE FROM {self.table_name} WHERE username = ?"
        cur.execute(command, (user_name,))
        con.commit()
        return (f"User{user_name} deleted successfully")

    def edit_user(self, user_name: str, email:str =None, height:float =None,weight:float = None,birthdate:date =None):
        con, cur = self.connect_database()

        update_fields = []
        update_values = []

        if email is not None:
            update_fields.append("email = ?")
            update_values.append(email)

        if height is not None:
            update_fields.append("height = ?")
            update_values.append(height)

        if weight is not None:
            update_fields.append("weight = ?")
            update_values.append(weight)

        if birthdate is not None:
            update_fields.append("birthdate = ?")
            update_values.append(birthdate)

        # Execute the update statement if there are any fields to update
        if update_fields:
            update_fields_str = ", ".join(update_fields)
            command = f"UPDATE {self.table_name} SET {update_fields_str} WHERE username = ?"
            update_values.append(user_name)
            cur.execute(command, update_values)
            con.commit()

        cur.execute(f"SELECT * FROM {self.table_name} WHERE username = ?", (user_name,))
        user_data = cur.fetchone()
        return(f"User {user_name} update successfully:{user_data}")

    def list_users(self):
        con, cur = self.connect_database()

        cur.execute(f"SELECT * FROM {self.table_name}")
        users=cur.fetchall()

        return users
        cur.close()
        con.close()

    def insert_meal(self, username:str, meal: Meal):
        self.create_meal_table()
        con, cur = self.connect_database()

        # Convert the meal time to a string representation because execute in SQL doesn't support object of type time
        meal_time_str = meal.time.strftime("%H:%M:%S")

        # Insert the meal data into the meals table along with the user_id
        cur.execute(
            f"INSERT INTO {self.meal_table} (username, meal_date, meal_time, meal, quantity, nutritional_info) VALUES (?, ?, ?, ?, ?, ?)",
            (username, meal.date, meal_time_str, meal.meal_name, meal.quantity, meal.nutritional_info))
        con.commit()

        return f"Meal {meal.meal_name} added successfully for user: {username}"

    def get_user_meals(self, username: str, start_date: date, end_date: date):
        con, cur = self.connect_database()

        # Retrieve the user_id based on the provided username
        cur.execute(f"SELECT username FROM {self.table_name} WHERE username = ?", (username,))
        user_id = cur.fetchone()

        if user_id is None:
            con.close()
            return f"No user found with the username: {user_id}"

        # Retrieve the meals for the user within the date range
        cur.execute(f"SELECT * FROM {self.meal_table} WHERE username = ? AND meal_date BETWEEN ? AND ? ", (username, start_date, end_date))
        meals = cur.fetchall()
        con.close()

        print(meals)
        return meals

    def delete_meal(self, username: str, meal_name: str):
        con, cur = self.connect_database()

        # Retrieve the user_id based on the provided username
        cur.execute(f"SELECT username FROM {self.table_name} WHERE username = ?", (username,))
        user_id = cur.fetchone()

        if user_id is None:
            con.close()
            return f"No user found with the username: {username}"

        # Check if the meal exists for the user with the specified name
        cur.execute(f"SELECT meal_date FROM {self.meal_table} WHERE username = ? AND meal = ?",
                    (username, meal_name))
        meal_date_str = cur.fetchone()

        if meal_date_str is None:
            con.close()
            return f"No meal found with the name '{meal_name}' for user '{username}'"

        # Convert meal_time_str to a datetime object
        meal_date = datetime.strptime(meal_date_str[0], "%Y-%m-%d")
        # Check if the meal_time is today's date
        today = date.today()
        if meal_date.date() != today:
            con.close()
            return f"Cannot delete a meal from a different date. Today is {today}."

        # Delete the meal for the user with the specified meal_name and meal_time
        cur.execute(f"DELETE FROM {self.meal_table} WHERE username = ? AND meal = ? AND meal_date = ?",
                    (username, meal_name, meal_date_str[0]))
        con.commit()
        con.close()

        return f"Meal '{meal_name}' deleted successfully for user: '{username}' on {meal_date_str[0]}"

    def edit_user_meal(self, username: str, meal_name: str, meal: Meal):
        con, cur = self.connect_database()

        # Retrieve the user_id based on the provided username
        cur.execute(f"SELECT username FROM {self.table_name} WHERE username = ?", (username,))
        user_id = cur.fetchone()

        if user_id is None:
            con.close()
            return f"No user found with the username: {username}"

        # Check if the meal exists for the user with the specified name
        cur.execute(f"SELECT meal_date, quantity FROM {self.meal_table} WHERE username = ? AND meal = ?",
                    (username, meal_name))
        meal_info = cur.fetchone()

        if meal_info is None:
            con.close()
            return f"No meal found with the name '{meal_name}' for user '{username}'"

        # Extract the meal time and quantity from the fetched row
        meal_date_str = meal_info[0]
        quantity = meal_info[1]

        # Convert meal_time_str to a datetime object
        meal_date = datetime.strptime(meal_date_str, "%Y-%m-%d").date()

        # Get today's date and the date of the previous day
        today = date.today()
        previous_day = today - timedelta(days=1)

        # Check if the meal_time is from today or the previous day
        if meal_date not in [today, previous_day]:
            con.close()
            return f"Cannot edit a meal from a different date. Only meals from today or the previous day can be edited."

        meal_date_obj = meal.date
        new_date_str = meal_date_obj.strftime("%Y-%m-%d")

        # Convert the meal time to a string representation because execute in SQL doesn't support object of type time
        meal_time_str = meal.time.strftime("%H:%M:%S")
        cur.execute(
            f"UPDATE {self.meal_table} SET meal = ?, quantity = ?, meal_date = ?, meal_time = ?, nutritional_info = ? WHERE username = ? AND meal = ? AND meal_date = ?",
            (meal.meal_name, meal.quantity, new_date_str, meal_time_str, meal.nutritional_info, username, meal_name, meal_date_str))
        con.commit()
        con.close()

        return f"Meal '{meal_name}' updated successfully for user: '{username}' on {meal_date_str}. " \
               f"New meal name: '{meal.meal_name}', new quantity: {meal.quantity},new date:{new_date_str} new time: {meal.time}"

    def get_meals_by_day(self, username: str, target_date: date):
        con, cur = self.connect_database()

        # Retrieve the user's ID using the provided username
        cur.execute(f"SELECT username FROM {self.table_name} WHERE username = ?", (username,))
        user_id = cur.fetchone()

        if user_id is None:
            con.close()
            return f"No user found with the username: {username}"

        target_date_str = target_date.strftime("%Y-%m-%d")
        # Query the meals table for the user's meals on the specified date
        cur.execute(
            f"SELECT meal, quantity, nutritional_info FROM {self.meal_table} WHERE username = ? AND DATE(meal_date) = ?",
            (username, target_date_str))
        meals = cur.fetchall()
        con.close()

        # Variables to store the total nutritional values in a specific day
        total_calories = 0
        total_fat=0
        total_protein=0
        total_carbohydrates=0
        total_fibers=0
        total_sugar=0

        # Extract the meal names and the other nutritional values from the fetched meals & calculate the total values
        extracted_meals = []
        for meal in meals:
            meal_name = meal[0]
            meal_quantity = meal[1]
            nutritional_info = meal[2]
            nutritional_info_list = json.loads(nutritional_info)
            nutritional_info_dict = nutritional_info_list[0]

            # Extracting the info that we need from the nutritional_info column from the table
            calories = nutritional_info_dict["calories"]# Access the calories value from the nutritional_info dictionary
            fat_total_g = nutritional_info_dict["fat_total_g"]
            protein_g = nutritional_info_dict["protein_g"]
            carbohydrates_total_g = nutritional_info_dict["carbohydrates_total_g"]
            fiber_g=nutritional_info_dict["fiber_g"]
            sugar_g=nutritional_info_dict["sugar_g"]

            # Calculating the total values for all day
            total_calories += calories
            total_fat += fat_total_g
            total_protein += protein_g
            total_carbohydrates +=carbohydrates_total_g
            total_fibers +=fiber_g
            total_sugar += sugar_g

            extracted_meals.append({"meal_name": meal_name, "meal_quantity": meal_quantity, "calories": calories, "fat_total_g": fat_total_g, "protein": protein_g, "fiber": fiber_g, "sugar": sugar_g})


        return (extracted_meals, f"For {target_date_str}:",
                f"Total calories are: {total_calories}", f"Totatl fats are {total_fat}",
                f"Total proteins are {total_protein}",
                f"Total carbohydrates are {total_carbohydrates}",
                f"Total fibers are {total_fibers}",
                f"Total sugar is {total_sugar}"
                )

    def generate_calories_pie_chart(self, username, target_date):
        con, cur = self.connect_database()

        cur.execute(
            f"SELECT meal, quantity, nutritional_info FROM {self.meal_table} WHERE username = ? AND DATE(meal_date) = ?",
            (username, target_date))
        meals = cur.fetchall()
        con.close()

        # Variables to store the total nutritional values in a specific day
        total_calories = 0
        total_fat = 0
        total_protein = 0
        total_carbohydrates = 0
        total_fibers = 0
        total_sugar = 0

        values = []
        labels =[]
        for meal in meals:
            meal_name = meal[0]
            meal_quantity = meal[1]
            nutritional_info = meal[2]
            nutritional_info_list = json.loads(nutritional_info)
            nutritional_info_dict = nutritional_info_list[0]

            # Extracting the info that we need from the nutritional_info column from the table
            calories = nutritional_info_dict["calories"]  # Access the calories value from the nutritional_info dictionary
            fat_total_g = nutritional_info_dict["fat_total_g"]
            protein_g = nutritional_info_dict["protein_g"]
            carbohydrates_total_g = nutritional_info_dict["carbohydrates_total_g"]
            fiber_g = nutritional_info_dict["fiber_g"]
            sugar_g = nutritional_info_dict["sugar_g"]

            total_calories += calories
            total_fat += fat_total_g
            total_protein += protein_g
            total_carbohydrates += carbohydrates_total_g
            total_fibers += fiber_g
            total_sugar += sugar_g

            labels.append({"l1": "calories", "l2": "fat", "l3": "protein", "l4": "carbohydrates", "l5": "fiber", "l6": "sugar"})
            values.append({"calories": total_calories, "fat_total_g": total_fat, "protein": total_protein, "carbohydrates": total_carbohydrates, "fiber": total_fibers, "sugar": total_sugar})


        # Create pie chart
        fig = px.pie(labels=labels, values=values, title='Calories Distribution')
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Customize chart appearance
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=2)))

        fig.update_layout(title='Nutritional info Distribution',
                          annotations=[dict(text=f'Total Nutritional values: {total_calories, total_fat, total_protein, total_carbohydrates, total_fibers, total_sugar}', showarrow=False)])

        # Display the chart
        return (fig.show())



class UserFile:
    def write_user(user: User):
        existing_users=[]
        path="src/myjson.json"
        #checking if the file exist and if it's empty
        if os.path.exists(path) and os.stat(path).st_size != 0:
            with open(path, "r") as jsonFile:
                existing_users=json.load(jsonFile) #putting in the existing_users list the list loaded from the json data file

        existing_users.append(user.dict()) #adding the user to the list of dicts, after transforming it to a dict

        with open(path, "w")as jsonFile:
            json.dump(existing_users, jsonFile) #transforms existing_users into a string and writes it to the json file

        return {"message":"User added successfully"}

    def get_user(self):
        path="src/myjson.json"
        with open(path, "r") as f:
            users=f.read()
        return users
    def delete_user(username: str):
        path="src/myjson.json"
        #loading the list of users that we have stored in our JSON file in existing_users varaible
        with open(path, "r") as f:
            existing_users=json.load(f)

        user_index=None
        #checking in existing_user list if any of the users has the username we are looking for
        for i, user in enumerate(existing_users):
            if user["username"] == username:
                #if so, we store the index of that user
                user_index = i
                break

        #and if the user with the specified username exists we'll remove it from the list
        if user_index is not None:
            existing_users.pop(user_index)

            #we rewrite the modified list with the user removed into the JSON file
            with open(path, "w") as f:
                json.dump(existing_users, f)

            return {"message": "User removed successfully"}
        #else we display error message
        else:
            return {"error" : "Couldn't find user"}

    def edit_user(username: str, email: str = None, height: float = None, weight: float=None) -> User:
        path="src/myjson.json"
        existing_users = []
        found_user = None

        if os.path.exists(path) and os.stat(path).st_size != 0:
            with open(path, "r") as jsonFile:
                existing_users = json.load(jsonFile)
        #find the user for which to update the data
        for user in existing_users:
            if user["username"] == username:
                found_user = user
                break
        #we update the data for the user
        if found_user:
            if email:
                found_user["email"] = email
            if height:
                found_user["height"] = height
            if weight:
                found_user["weight"] = weight
            #update the JSON file with the new updates for the user
            with open(path, "w")as jsonFile:
                json.dump(existing_users, jsonFile)

            return User(**found_user)
        else:
            raise ValueError(f"User with username {username} not found")