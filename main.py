import os
from enum import Enum
from db import get_db
import sys

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
        return str(self.first_name + ' ' + self.last_name + ' ' + self.age + ' ' + self.sex + ' ' + self.height + ' ' + self.weight + ' ' + self.activity_level)
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
    
    # parse input to screen if user needs to be enrolled
    # this should be some type of state when first connecting
    # then a constant state so we don't have to keep reverifying the user
    new_use = input("Are you a new or old User?")
    new_use = new_use.replace(" ", "")
    new_use = new_use.lower()
    
    if (new_use == "yes"):
        print("Great! Would you like to signup?")
        inputs = input()
        inputs = input.lower()
        if inputs == 'no':
            print('Bye!')
            return
            
        # define sex instead of gender
        # implement new user system registration
        first_name = input("Welcome! To get started off, what is your first name?")
        last_name = input("Great! Now what is your last name?")
        sex = input("What is you sex? Male/Female/NA")
        sex = sex.lower()
        if sex == 'na':
            sex = 'male'
        height = int(input("Awesome. Next, what is your height in inches?"))
        starting_weight = int(input("What is your current weight in lbs?"))
        Activity_type = int(input("How active would you say you are? 1. Sedentary: 0-1 days, 2. Light: 1-3 days, 3. Moderate: 3-4 days, 4. Very: 4-5 days, 5.  Extremely:5-7 days?"))
        #For men: BMR = 66.5 + (13.75 × weight in kg) + (5.003 × height in cm) - (6.75 × age)
        #For women: BMR = 655.1 + (9.563 × weight in kg) + (1.850 × height in cm) - (4.676 × age)
        #Sedentary (little or no exercise): calories = BMR × 1.2;
        #Lightly active (light exercise/sports 1-3 days/week): calories = BMR × 1.375;
#       Moderately active (moderate exercise/sports 3-5 days/week): calories = BMR × 1.55;
        #Very active (hard exercise/sports 6-7 days a week): calories = BMR × 1.725; and
        #If you are extra active (very hard exercise/sports & a physical job): calories = BMR × 1.9.
    else:
        first_name = input("Welcome Back! What's your first name?")
        last_name = input("Awesome. What's your last name?")
        # also include a check to make sure that user is found
        # query to database to get user information about calories for the day.
        exit = False
        # stay stuck inl loop until user wants to leave
        while (not exit):
            # this includes all food additions, food type commands, calorie asks, etc.
            inputs = input()
            inputs = inputs.lower()
            if (inputs == 'exit'):
                break
            inputs = inputs.lower()
            # Ate will be a keyword for addings food eaten by the user
            # how will indicate that we either need to check the food api for calorie count or check how many calories are left
            # so user will ask "how many calories left", so "left" is the keyword for user calorie check
            if inputs.find('ate') != -1:
                #TODO: add query to nutritionix and add food entry
                pass
            elif inputs.find('how') != -1:
                if inputs.find('left') != 1:
                    pass  # query use database to find remaining calories and macros
                else:
                    pass
                    # query nutritionix to find nutritional information
            elif inputs.find('update') != -1:
                pass # user can update their preferences/activity level/weight
            else:
                continue
            # keyword search for adding food, asking how many macros left, and asking nutritional info about food,




def db_check():
    connection = get_db()
    users = connection.execute(
        "SELECT * "
        "FROM users "
    ).fetchall()

    if users:
        for user in users:
            print(user['username'])


def main():
    user_onboard()

if __name__ == "__main__":
    db_check()
