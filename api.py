import requests
import json


def api_request(input):
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
    try:
        query = {
            "query": input
        }
        r = requests.post(end_pt_url, headers=HEADERS, json=query)
        data = json.loads(r.text)
        # new_string = json.dumps(data,indent=2)
        # print(new_string)

        return data["foods"]

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return 0


if __name__ == "__main__":
    test_query = {
        "query": "i ate 500 grams of chicken"
    }
    api_request(test_query)
