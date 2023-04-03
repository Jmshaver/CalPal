from sentence_transformers import util, SentenceTransformer
import pandas as pd
from api import api_request
from db import get_db
from speak import speak
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
