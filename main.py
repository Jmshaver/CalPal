import os
from enum import Enum
from db import get_db
import sys
from api import api_request
from db import get_db


# USE SNAKE CASE FOR ALL VARIABLES


class State(Enum):
    START = 1


# create a class to process user boarding process, record their
# name, sex, height, weight and activity level


class User:
    # maybe use enum for activity level
    class activity_level(Enum):
        LIGHTLY_ACTIVE = 1
        MODERATELY_ACTIVE = 2
        VERY_ACTIVE = 3

    def __init__(self, first_name, last_name, age, sex, height, weight, activity_level):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.height = height
        self.weight = weight
        self.activity_level = activity_level

    # return userinfo
    def __str__(self):
        return str(
            self.first_name + ' ' + self.last_name + ' ' + self.age + ' ' + self.sex + ' ' + self.height + ' ' + self.weight + ' ' + self.activity_level)

    # getters portion

    def get_first_name(self):
        return self.name

    def get_last_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_sex(self):
        return self.sex

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_activity_level(self):
        return self.activity_level

    # setters portion

    def update_first_name(self, first_name):
        self.first_name = first_name

    def update_last_name(self, last_name):
        self.last_name = last_name

    def update_age(self, age):
        self.age = age

    def update_sex(self, sex):
        self.sex = sex

    def update_height(self, height):
        self.height = height

    def update_weight(self, weight):
        self.weight = weight

    def update_activity_level(self, activity_level):
        self.activity_level = activity_level


def user_onboard():
    # user onboard procedure, will change this to a different function later
    print("Hello")
    connection = get_db()
    # parse input to screen if user needs to be enrolled
    # this should be some type of state when first connecting
    # then a constant state so we don't have to keep reverifying the user
    new_use = input("Are you a new or old User?")
    new_use = new_use.replace(" ", "")
    new_use = new_use.lower()

    if (new_use == "new"):
        print("Great! Would you like to signup?")
        inputs = input()
        inputs = inputs.lower()
        if inputs == 'no':
            print('Bye!')
            return

        # define sex instead of gender
        # implement new user system registration
        first_name = input(
            "Welcome! To get started off, what is your first name?")
        last_name = input("Great! Now what is your last name?")

        sex = None
        while sex not in ['male', 'female', 'other']:
            sex = input("What is you sex? Male/Female/NA")
            sex = sex.lower()

        height = int(input("Awesome. Next, what is your height in inches?"))
        starting_weight = int(input("What is your current weight in lbs?"))
        # TODO: age can change over time, so we should update it every day, we use age now but in long run this should be a date
        age = int(input("How old are you?"))

        activity_type = None
        while activity_type not in [1, 2, 3, 4, 5]:
            activity_type = int(input(
                "How active would you say you are? 1. Sedentary: 0-1 days, 2. Light: 1-3 days, 3. Moderate: 3-4 days, 4. Very: 4-5 days, 5.  Extremely:5-7 days?"))
        activity_type = ['SEDENTARY', 'LIGHT', 'MODERATE',
                         'VERY', 'EXTREMELY'][activity_type]
        calorie_goal = calculate_intake(height, starting_weight, age, sex, activity_type)
        # TODO add user's real info
        insert_query = "INSERT INTO users (First_name, Last_name, Height, Starting_Weight, Age, Activity_type, Sex, Calorie_goal) VALUES (?, ?, ?, ?, ?, ?, ?,?)"
        values = (first_name, last_name, height, starting_weight, age, activity_type, sex, calorie_goal)
        connection.execute(insert_query, values)
        connection.commit()

        print("Account Created. Welcome to CalPal")

    else:

        first_name = input("Welcome Back! What's your first name?")
        last_name = input("Awesome. What's your last name?")
        # also include a check to make sure that user is found
        # query to database to get user information about calories for the day.
        # stay stuck inl loop until user wants to leave

        insert_query = "SELECT USER_ID FROM users WHERE First_name = ? AND Last_name = ?"
        values = (first_name, last_name)
        user = connection.execute(insert_query, values).fetchone()
        if user is None:
            print('You are not in the database please sign up')

        user_id = user['USER_ID']
        while (True):
            # this includes all food additions, food type commands, calorie asks, etc.
            print("How can I help you? ")
            inputs = input()
            inputs = inputs.lower()
            if (inputs == 'exit'):
                break
            inputs = inputs.lower()
            # Ate will be a keyword for addings food eaten by the user
            # how will indicate that we either need to check the food api for calorie count or check how many calories are left
            # so user will ask "how many calories left", so "left" is the keyword for user calorie check
            if inputs.find('ate') != -1:
                foods = api_request(inputs)

                for food in foods:
                    food_name = food["food_name"]
                    cal_count = food["nf_calories"]
                    fat_count = food["nf_total_fat"]
                    protein_count = food["nf_protein"]
                    carb_count = food["nf_total_carbohydrate"]
                    connection.execute(
                        "INSERT INTO Food_Intake (USER_ID, Food_Name ,Calories,Protein,Carbohydrates,Fats ) "
                        "VALUES (? ,?, ?, ?, ?, ? ) ",
                        (user_id, food_name, cal_count,
                         fat_count, protein_count, carb_count)
                    )
                    connection.commit()
                    print(
                        f"{food_name} was logged. It was {cal_count} calories with {protein_count} grams of protein, {carb_count} grams of carbs and {fat_count} grams of fat")

                # TODO tell the user how their daily goal is going
                pass
            elif inputs.find('how') != -1:
                if inputs.find('left') != -1:
                    pass  # TODO query use database to find remaining calories and macros
                else:
                    # TODO input needs to be modified so the api does not return 1 calorie
                    foods = api_request(inputs)

                    for food in foods:
                        food_name = food["food_name"]
                        cal_count = food["nf_calories"]
                        fat_count = food["nf_total_fat"]
                        protein_count = food["nf_protein"]
                        carb_count = food["nf_total_carbohydrate"]

                        print(
                            f"{food_name} has {cal_count} calories with {protein_count} grams of protien, {carb_count} grams of carbs and {fat_count} grams of fat")

            elif inputs.find('update') != -1:
                pass  # TODO user can update their preferences/activity level/weight
            elif inputs == "thanks calpal":
                print("Glad to help. You are making great progress")
                break
            else:
                print(
                    "I don't understand what you are trying to do. Say 'Thanks CalPal to Exit'")
                continue
            # TODO keyword search for adding food, asking how many macros left,


'''
Requires: stats of a user. Their height, weight, age, and activity level to calculate their daily calorie intake
Modifies: Nothing
Effects: Returns the daily calorie intake of the user
'''


def calculate_intake(height, weight, age, sex, activity_level):
    # For men: BMR = 66.5 + (13.75 × weight in kg) + (5.003 × height in cm) - (6.75 × age)
    # For women: BMR = 655.1 + (9.563 × weight in kg) + (1.850 × height in cm) - (4.676 × age)
    # Sedentary (little or no exercise): calories = BMR × 1.2;
    # Lightly active (light exercise/sports 1-3 days/week): calories = BMR × 1.375;
    # Moderately active (moderate exercise/sports 3-5 days/week): calories = BMR × 1.55;
    # Very active (hard exercise/sports 6-7 days a week): calories = BMR × 1.725; and
    # If you are extra active (very hard exercise/sports & a physical job): calories = BMR × 1.9.

    # first we need to convert height and weight to metric
    height = height * 2.54
    weight = weight * 0.453592

    # calculate BMR
    bmr = 0
    if sex == "male":
        bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
    # default to use female otherwise
    else:
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

    # calculate calorie intake
    if activity_level == "SEDENTARY":
        return bmr * 1.2
    elif activity_level == "LIGHT":
        return bmr * 1.375
    elif activity_level == "MODERATE":
        return bmr * 1.55
    elif activity_level == "VERY":
        return bmr * 1.725
    else:
        return bmr * 1.9


def main():
    user_onboard()


if __name__ == "__main__":
    main()
