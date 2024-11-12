import json
import requests
import os
from datetime import datetime

# Load train data from trains_en.json
with open('trains_en.json', 'r', encoding='utf-8') as file:
    train_data = json.load(file)

# Extract train names and models
trains = [(train.rsplit('(', 1)[0].strip(), train.split('(')[-1].split(')')[0]) for train in train_data['trains']]

# Date for the request (can be modified as needed)
departure_date = "2024-11-12"

# Create output directory based on the current date and time
output_directory = f"train_info_responses"
os.makedirs(output_directory, exist_ok=True)

# Function to make a POST request and save the response
def fetch_and_save_response(train_name, model):
    url = "https://railspaapi.shohoz.com/v1.0/web/train-routes"
    payload = {
        "model": model,
        "departure_date_time": departure_date
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        
        # Format filename as trainname_trainmodel.json
        safe_train_name = train_name.replace(" ", "_").replace("/", "-")
        output_filename = os.path.join(output_directory, f"{safe_train_name}_{model}.json")
        
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            json.dump(response_data, output_file, indent=4)
        
        print(f"Saved: {output_filename}")
    else:
        print(f"Failed to fetch data for {train_name} (Model: {model}). Status code: {response.status_code}")

# Fetch and save responses for each train
for train_name, model in trains:
    fetch_and_save_response(train_name, model)