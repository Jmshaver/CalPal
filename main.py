import os
from db import get_db
from calpal import CalPal
connection = get_db()


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


def user_onboard(first_name, last_name):
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
    calorie_goal = calculate_intake(
        height, starting_weight, age, sex, activity_type)
    insert_query = "INSERT INTO users (First_name, Last_name, Height, Starting_Weight, Age, Activity_type, Sex, Calorie_goal) VALUES (?, ?, ?, ?, ?, ?, ?,?)"
    values = (first_name, last_name, height, starting_weight,
              age, activity_type, sex, calorie_goal)
    connection.execute(insert_query, values)
    connection.commit()

    user_id = connection.execute(
        "SELECT USER_ID FROM users WHERE First_name = ? AND Last_name = ?", (first_name, last_name)).fetchone()['USER_ID']
    print("Account Created. Welcome to CalPal")

    return user_id


def get_current_user():
    filename = "current_user.txt"
    user_id = ''

    try:
        with open(filename, "r") as f:
            user_id = f.read()
            if len(user_id) == 0:
                raise FileNotFoundError

    except FileNotFoundError:

        first_name = input("What's your first name?")
        last_name = input("Awesome. What's your last name?")
        # print(first_name, last_name)
        user_id = connection.execute(
            "SELECT USER_ID FROM users WHERE First_name = ? AND Last_name = ?", (first_name, last_name)).fetchone()

        if user_id is None:
            user_id = user_onboard(first_name, last_name)
        else:
            user_id = user_id['USER_ID']

        with open(filename, 'w') as f:
            f.write(str(user_id))

    # print(user_id)
    return user_id


if __name__ == "__main__":
    print("Starting")
    user_id = get_current_user()
    calpal = CalPal(user_id)

    while True:
        input_phrase = input("How can I help\n")
        input_phrase.lower()
        intent = calpal.get_intent(input_phrase)
        if intent == 0:
            break
        else:
            calpal.handle_intent(intent, input_phrase)
