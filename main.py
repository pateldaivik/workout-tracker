import requests
from datetime import datetime
import os
from config import sheety
os.environ["APP_ID"] = '902811ac'
os.environ['API_KEY'] ='62829eed531cbc31e5dad10d99f67de2'
APP_ID =os.getenv('APP_ID')
API_KEY =os.getenv('API_KEY')
GENDER = 'Male'
WEIGHT_KG = 75
HEIGHT_CM = 160
AGE = 22

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me which exercises you did: ")
sheet_endpoint = sheety['endpoint']

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    bearer_sheety = sheety['bearer']
    bearer_headers = {
        "Authorization": bearer_sheety
    }
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)
    print(sheet_response.text)