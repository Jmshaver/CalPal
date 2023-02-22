import requests
import json
from db import get_db


def api_request(query):
    # Nutritionix API
    end_pt_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    app_id = 'a68ff72b'
    app_key = '7d72b7a7492cfb38114e8cbfebbe841b'
    HEADERS = {
        'x-app-id': app_id,
        'x-app-key': app_key,
        'content-type': 'application/json'
    }

    # test command

    r = requests.post(end_pt_url, headers=HEADERS, json=query)

    data = json.loads(r.text)
    #new_string = json.dumps(data,indent=2)
    # print(new_string)
    connection = get_db()

    for foods in data["foods"]:
        food_name = foods["food_name"]
        cal_count = foods["nf_calories"]
        fat_count = foods["nf_total_fat"]
        protein_count = foods["nf_protein"]
        carb_count = foods["nf_total_carbohydrate"]

        connection.execute(
            "INSERT INTO Food_Intake (USER_ID, Food_Name ,Calories,Protein,Carbohydrates,Fats ) "
            "VALUES (? ,?, ?, ?, ?, ? ) ",
            (1, food_name, cal_count, fat_count, protein_count, carb_count)
        )
        connection.commit()
        connection.close()
        print(food_name, cal_count, protein_count, carb_count, fat_count)


if __name__ == "__main__":
    test_query = {
        "query": "i ate 500 grams of chicken"
    }
    api_request(test_query)
