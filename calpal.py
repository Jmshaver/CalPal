
from sentence_transformers import util, SentenceTransformer
import pandas as pd
from api import api_request
from db import get_db
from speak import speak, get_audio
import datetime
connection = get_db()

model = SentenceTransformer('multi-qa-MiniLM-L6-dot-v1')


class CalPal:
    def __init__(self, user_id, threshold=.4, intent_file='intent_phrases.csv'):
        self.user_id = user_id
        self.intent_df = pd.read_csv(intent_file)
        self.threshold = threshold
        # print(self.intent_df.head())
        self.intent_embeddings = model.encode(self.intent_df['phrase'])
    
    def calculate_intake(height, weight, age, sex, activity_level, dietType):
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
            bmr *= 1.2
        elif activity_level == "LIGHT":
            bmr *= 1.375
        elif activity_level == "MODERATE":
            bmr *= 1.55
        elif activity_level == "VERY":
            bmr *= 1.725
        else:
            bmr *= 1.9
        if dietType == "BALANCED":
            protein_goal = 0.65*(weight/0.453592)
            fat_goal = (0.3 *  bmr) / 9
            carb_goal = (bmr - fat_goal*9 - protein_goal*4) / 4
        elif dietType == "HIGH PROTEIN":
            protein_goal = (weight/0.453592)
            fat_goal = (0.3*bmr) / 9
            carb_goal = (bmr - fat_goal*9 - protein_goal*4) / 4
        else:
            protein_goal = 0.8*(weight/0.453592)
            fat_goal = (0.45*bmr) / 9
            carb_goal = (bmr - fat_goal*9 - protein_goal*4) / 4

        return bmr, protein_goal, fat_goal, carb_goal
    def get_intent(self, phrase):
        sentence_embedding = model.encode(phrase)
        # Print the embeddings
        max_cos_sim = -2.3
        max_cos_sim_index = -1
        for index, sentence in enumerate(self.intent_embeddings):
            sim = util.cos_sim(sentence, sentence_embedding)
            # print("sim for ", self.intent_df['phrase'][index], " is ", sim)
            if sim > max_cos_sim:
                max_cos_sim = sim
                max_cos_sim_index = index

        if max_cos_sim < self.threshold:
            print("did not match intent")
            return -1

        print("intent: ", self.intent_df['intent'][max_cos_sim_index])
        print("closest to:", self.intent_df['phrase'][max_cos_sim_index])
        return self.intent_df['intent'][max_cos_sim_index]

    def ate_food_intent(self, input_phrase):
        foods = api_request(input_phrase)
        if (not isinstance(foods, list)) or len(foods) == 0:
            speak("i don't know that food")
            return
        outputs = []
        for food in foods:
            food_name = food["food_name"]
            cal_count = food["nf_calories"]
            fat_count = food["nf_total_fat"]
            protein_count = food["nf_protein"]
            carb_count = food["nf_total_carbohydrate"]
            connection.execute(
                "INSERT INTO Food_Intake (USER_ID, Food_Name ,Calories,Protein,Carbohydrates,Fats ) "
                "VALUES (? ,?, ?, ?, ?, ? ) ",
                (self.user_id, food_name, cal_count,
                    fat_count, protein_count, carb_count)
            )
            print((self.user_id, food_name, cal_count,
                   fat_count, protein_count, carb_count))
            connection.commit()
            outputs.append(
                f"{food_name} was logged. It was {cal_count} calories with {protein_count} grams of protein, {carb_count} grams of carbs and {fat_count} grams of fat")
        speak(outputs)

    def update_info_intent(self):
        sex = None
        while sex not in ['male', 'female', 'other']:
            speak("What is you sex? Male/Female/NA")
            sex = get_audio()
            sex = sex.lower()
            if sex == 'mail':
                sex = 'male'

        speak("Awesome. Next, what is your height in inches?")
        height = int(get_audio())
        speak("What is your current weight in lbs?")
        starting_weight = int(get_audio())
        # TODO: age can change over time, so we should update it every day, we use age now but in long run this should be a date
        speak("How old are you?")
        age = int(get_audio())

        activity_type = None
        options = ['sedentary',
                'light',
                'moderate',
                'very',
                'extremely']
        while activity_type not in options:
            speak("How active would you say you are? 1. Sedentary: 0-1 days, 2. Light: 1-3 days, 3. Moderate: 3-4 days, 4. Very: 4-5 days, 5.  Extremely:5-7 days?")
            activity_type = get_audio()
            print(activity_type)
            print(options)
        activity_type = activity_type.upper()
        dietType = None
        options_diet = ['balanced', 'high protein', 'low carb']
        while dietType not in options_diet:
            speak('What Kind of Diet would you like to have? 1. Balanced, 2. High Protein, 3. Low Carb ')
            dietType = get_audio()
            print(dietType)
            print(options_diet)
        dietType = dietType.upper()
        calorie_goal, protein_goal, fat_goal, carb_goal =  self.calculate_intake(height, starting_weight, age, sex, activity_type, dietType)

        connection.execute("UPDATE users SET Height = ? , Starting_Weight = ?, Age = ?, Activity_type = ?, Sex = ?, Calorie_goal = ?, Diet_type = ?, Protein_goal = ?, Fat_goal=? , Carb_goal = ? WHERE USER_ID = ? ", (height, starting_weight, age,activity_type, sex, calorie_goal, dietType, protein_goal, fat_goal, carb_goal))
        connection.commit()
        speak("User information successfully updated")

    def current_progress_intent(self):
        # datetime seem to take computer timezone while sql uses gmt
        # this means 8pm to 4am will have errors
        today = datetime.date.today()
        macro_info = connection.execute("SELECT SUM(Protein) as protein,  SUM(Carbohydrates) as carbs,  SUM(Fats) as fats FROM Food_Intake "
                                        "WHERE date(CREATED) = ? AND USER_ID = ?", (today, self.user_id)).fetchone()

        # check if the user has eaten anything
        if macro_info['fats'] is None:
            speak("You have not eaten anything today")
            return

        user_calorie_goal = connection.execute(
            "SELECT Calorie_goal FROM users WHERE USER_ID = ?", (self.user_id,)).fetchone()['Calorie_goal']
        calories_eaten_today = connection.execute("SELECT SUM(Calories) as total FROM Food_Intake "
                                                  "WHERE date(CREATED) = ? AND USER_ID = ?", (today, self.user_id)).fetchone()['total']

        user_calorie_goal = round(user_calorie_goal)
        calories_eaten_today = round(calories_eaten_today)
        if user_calorie_goal - calories_eaten_today >= 0:
            speak(
                f"Your goal is {user_calorie_goal} calories and you have eaten {calories_eaten_today} calories you have {user_calorie_goal - calories_eaten_today} calories to go. Keep it up!")
        else:
            speak(
                f"Your goal is {user_calorie_goal} calories and you have eaten {calories_eaten_today} calories you are over by { calories_eaten_today - user_calorie_goal} calories.")
        speak("Your macros are")
        speak(f"Protein: {macro_info['protein']}g")
        speak(f"Carbohydrates: {macro_info['carbs']}g")
        speak(f"Fats: {macro_info['fats']}g")

    def food_lookup_intent(self, input_phrase):
        inputs = input_phrase.replace("how", "").replace(
            "calories", "").replace("many", "").lstrip()

        foods = api_request(inputs)

        if isinstance(foods, int):
            speak("Sorry cant find that food")
            return

        for food in foods:
            food_name = food["food_name"]
            cal_count = food["nf_calories"]
            fat_count = food["nf_total_fat"]
            protein_count = food["nf_protein"]
            carb_count = food["nf_total_carbohydrate"]

            speak(
                f"{food_name} has {cal_count} calories with {protein_count} grams of protien, {carb_count} grams of carbs and {fat_count} grams of fat")

    def list_eaten_foods_intent(self):
        # datetime seem to take computer timezone while sql uses gmt
        # this means 8pm to 4am will have errors
        today = datetime.date.today()
        foods = connection.execute("SELECT Food_name FROM Food_Intake "
                                   "WHERE date(CREATED) = ? AND USER_ID = ?", (today, self.user_id)).fetchall()
        if len(foods) == 0:
            speak("You have not eaten anything today")
            return
        speak("You have eaten")
        output = []
        for food in foods:
            output.append(food['Food_name'])
        speak(','.join(output))

    def handle_intent(self, intent, input_phrase):
        # print("handling intent ", intent)
        if intent == -1:
            speak("Sorry I don't understand what you are asking")
        elif intent == 0:  # exit calpal
            print("This should never be called")
        elif intent == 1:  # example: I just ate a whopper
            self.ate_food_intent(input_phrase)
        elif intent == 2:  # example: Have I reached my calorie goal today
            self.current_progress_intent()
        elif intent == 3:  # example: How many calories are in a whopper
            self.food_lookup_intent(input_phrase)
        elif intent == 4:  # example: what foods have I eaten today
            self.list_eaten_foods_intent()


def main():
    sentence1 = "I like turtles"
    pal = CalPal()
    pal.get_intent(phrase=sentence1)


if __name__ == "__main__":

    main()
