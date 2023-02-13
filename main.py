import os
from enum import Enum
from db import get_db
import sys

# USE SNAKE CASE FOR ALL VARIABLES

# create a class to process user boarding process, record their
# name, sex, height, weight and activity level


class State(Enum):
    START = 1


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
        self.gender = sex
        self.height = height
        self.weight = weight
        self.activity_level = activity_level

    # TODO: this need to change for debugging
    def __str__(self):
        return
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
        # define sex
        # implement new user system registration
    else:
        first_name = input("Welcome Back! What's your first name?")
        last_name = input("Awesome. What's your last name?")
        # also include a check to make sure that user is found
        # query to database to get user information about calories for the day.
        exit = False
        # stay stuck inl loop until user wants to leave
        while (not exit):
            # this includes all food additions, food type commands, calorie asks, etc.
            input = input()
            input = input.lower()
            if (input == 'exit'):
                break
            # keyword search for adding food, asking how many macros left, and asking nutritional info about food,


def main():
    user_onboard()


def db_check():
    connection = get_db()
    users = connection.execute(
        "SELECT * "
        "FROM users "
    ).fetchall()

    if users:
        for user in users:
            print(user['username'])


if __name__ == "__main__":
    db_check()
