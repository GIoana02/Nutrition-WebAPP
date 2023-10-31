# Nutrition API Application

## Overview

The Nutrition API Application is a simple application that allows users to register, manage their profiles, and track their meals' nutritional values using an external API. This README will provide instructions on how to set up and use the application effectively.

### The Application provides two management routers that have specific endpoints:
### 1.  User Management 

- Add User
- Get User
- Delete User
- Edit User
- List Users
### 2.  Meals Management

- Insert Meal
- Get User Meals
- Delete Meal
- Edit User Meal
- Get Meals By Day

### API Integration


The application integrates with the [Nutrition API](https://api.api-ninjas.com/v1/nutrition) to calculate nutritional values for meals.
## Installation


1. Clone the repository:

   ```
   git clone https://github.com/GIoana02/Nutrition-WebAPP.git
   cd Nutrition-WebAPP

2. Install docker (https://docs.docker.com/desktop/)
 

3. Build docker image:
   ```
   docker build -t nutritionapp .

4. Start container:
   ```
   docker run -d --name nutritionapp -p 8000:8000 --mount type=bind,source="$(pwd)/src",target=/home/nutrition_app/src nutritionapp
   
5. Open browser and access `localhost:8000` :

   http://localhost:8000/


6. To see the Swagger UI documentation you need to append `/docs` on the url:
   
   http://localhost:8000/docs


   You can access if needed the logs of the docker container by using the following command:
        
   ```
         docker logs -f nutritionapp
   ```
## Technologies

- Back-end: FastAPI, Python, Docker
- Database: SQLite
