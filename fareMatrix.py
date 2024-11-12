import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama for colored text output
init(autoreset=True)

# Directory containing processed JSON files
processed_dir = 'processed'
target_train_model = "707"  # This can be set to match the desired train model

# Date for the journey in the correct format
date_of_journey = "19-Nov-2024"  # This can be modified as needed

# Collect train data from the processed folder
train_data = None
for file_name in os.listdir(processed_dir):
    if file_name.endswith('.json'):
        with open(os.path.join(processed_dir, file_name), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data['data']['train_model'] == target_train_model:
                train_data = data['data']
                break

if not train_data:
    print(f"{Fore.RED}No matching train data found for model {target_train_model}")
    exit()

# Extract station list and days from the train data
stations = [route['city'] for route in train_data['routes']]
days = train_data['days']
train_name = train_data['train_name']

# Check if the date of journey is an off day for the train
date_obj = datetime.strptime(date_of_journey, "%d-%b-%Y")
day_of_week = date_obj.strftime("%a")  # Get the abbreviated day name (e.g., "Mon", "Tue")

if day_of_week not in days:
    print(f"{Fore.YELLOW}The train '{train_name}' (Model: {target_train_model}) does not run on {day_of_week}. Please choose another date.")
    exit()

print(f"{Fore.GREEN}Train Name: {train_name}")
print(f"Train Model: {target_train_model}")
print(f"Running Days: {', '.join(days)}")
print(f"Stations: {', '.join(stations)}\n")

# List of seat types for Bangladesh Railway
seat_types = ["AC_B", "AC_S", "SNIGDHA", "F_BERTH", "F_SEAT", "F_CHAIR",
              "S_CHAIR", "SHOVAN", "SHULOV", "AC_CHAIR"]

# Function to get seat availability for a specific route
def get_seat_availability(from_city, to_city):
    url = f"https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2"
    params = {
        "from_city": from_city,
        "to_city": to_city,
        "date_of_journey": date_of_journey,
        "seat_class": "SHULOV"  # Modify this as needed
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        response_data = response.json()
        trains = response_data.get("data", {}).get("trains", [])
        
        for train in trains:
            if train.get("train_model") == target_train_model:
                seat_info = {seat_type: {"online": 0, "offline": 0, "fare": 0} for seat_type in seat_types}
                for seat in train.get("seat_types", []):
                    seat_type = seat["type"]
                    if seat_type in seat_info:
                        seat_info[seat_type] = {
                            "online": seat["seat_counts"]["online"],
                            "offline": seat["seat_counts"]["offline"],
                            "fare": seat["fare"]
                        }
                print(f"{Fore.GREEN}Successfully fetched data for {from_city} to {to_city}")
                return from_city, to_city, seat_info
        
        # If the train is not found in the response, return empty data
        print(f"{Fore.YELLOW}No data found for {target_train_model} between {from_city} and {to_city}")
        return from_city, to_city, None
    
    # If the response fails, log the error and return None
    print(f"{Fore.RED}Failed to fetch data for {from_city} to {to_city}. Status code: {response.status_code}")
    return from_city, to_city, None

# Create a dictionary to store fare matrices for each seat type
fare_matrices = {seat_type: {from_city: {} for from_city in stations} for seat_type in seat_types}

# Use ThreadPoolExecutor for concurrent data fetching
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(get_seat_availability, from_city, to_city)
        for i, from_city in enumerate(stations)
        for j, to_city in enumerate(stations)
        if i < j  # Only consider forward pairs (origin to destination)
    ]
    
    for future in as_completed(futures):
        from_city, to_city, seat_info = future.result()
        if seat_info:
            for seat_type in seat_types:
                fare_matrices[seat_type][from_city][to_city] = seat_info.get(seat_type, {"online": 0, "offline": 0, "fare": 0})
        else:
            for seat_type in seat_types:
                fare_matrices[seat_type][from_city][to_city] = {"online": 0, "offline": 0, "fare": 0}
            print(f"{Fore.YELLOW}No seat data available for {from_city} to {to_city}, set to zero.")

# Function to display the table in chunks to fit the terminal window
def print_table_in_chunks(table_data, header, chunk_size=12):
    for start in range(1, len(header), chunk_size):
        # Define the end of the current chunk
        end = min(start + chunk_size, len(header))
        
        # Print the header and table data for the current chunk
        current_header = header[:1] + header[start:end]
        current_table_data = [row[:1] + row[start:end] for row in table_data]
        
        # Print the chunk using tabulate
        print(tabulate(current_table_data, headers=current_header, tablefmt="grid"))

# Display the fare matrices in chunks to fit terminal width
for seat_type in seat_types:
    has_seats = any(
        any((seat_info["online"] + seat_info["offline"]) > 0 for seat_info in fare_matrices[seat_type][from_city].values())
        for from_city in stations
    )
    
    if has_seats:
        print(f"\n{'-'*50}")
        print(f"Fare Matrix Representation for Seat Type: {seat_type}")
        print(f"{'-'*50}")

        table_data = []
        header = ["From\\To"] + stations
        
        for i, from_city in enumerate(stations):
            row = [from_city]
            for j, to_city in enumerate(stations):
                if i == j or i > j:
                    row.append("")
                else:
                    seat_info = fare_matrices[seat_type][from_city].get(to_city, {"online": 0, "offline": 0})
                    available_seats = seat_info["online"] + seat_info["offline"]
                    row.append(available_seats if available_seats > 0 else "")
            table_data.append(row)
        
        # Print the table in chunks
        print_table_in_chunks(table_data, header, chunk_size=12)

print("\nOnly fare matrices with available seats have been displayed.")