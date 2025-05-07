import json, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
from colorama import init, Fore, Style
from datetime import datetime
from collections import deque

# Initialize colorama for colored text output
init(autoreset=True)

# Target train model and journey date
target_train_model = "745"  # This can be set to match the desired train model

# Date for the journey in the correct format
date_of_journey = "15-Nov-2024"  # This can be modified as needed

# Convert date_of_journey to API required format (YYYY-MM-DD)
date_obj = datetime.strptime(date_of_journey, "%d-%b-%Y")
api_date_format = date_obj.strftime("%Y-%m-%d")

# Fetch train data from API
def fetch_train_data(model, departure_date):
    url = "https://railspaapi.shohoz.com/v1.0/web/train-routes"
    payload = {
        "model": model,
        "departure_date_time": departure_date
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('data')
    else:
        print(f"{Fore.RED}Failed to fetch train data. Status code: {response.status_code}")
        return None

# Collect train data
train_data = fetch_train_data(target_train_model, api_date_format)

if not train_data:
    print(f"{Fore.RED}No matching train data found for model {target_train_model}")
    exit()

# Extract station list and days from the train data
stations = [route['city'] for route in train_data['routes']]
days = train_data['days']
train_name = train_data['train_name']

# Check if the date of journey is an off day for the train
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
                seat_info = {seat_type: {"online": 0, "offline": 0, "fare": 0, "vat_amount": 0} for seat_type in seat_types}
                for seat in train.get("seat_types", []):
                    seat_type = seat["type"]
                    if seat_type in seat_info:
                        seat_info[seat_type] = {
                            "online": seat["seat_counts"]["online"],
                            "offline": seat["seat_counts"]["offline"],
                            "fare": float(seat["fare"]),
                            "vat_amount": float(seat["vat_amount"])
                        }
                print(f"{Fore.GREEN}Successfully fetched data for {from_city} to {to_city}")
                return from_city, to_city, seat_info

        # If the train is not found in the response, return empty data
        print(f"{Fore.YELLOW}No data found for {target_train_model} between {from_city} and {to_city}")
        return from_city, to_city, None

    # If the response fails, log the error and return None
    print(f"{Fore.RED}Failed to fetch data for {from_city} to {to_city}. Status code: {response.status_code}")
    return from_city, to_city, None

# Create a dictionary to store seat matrices for each seat type
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
        end = min(start + chunk_size, len(header))
        current_header = header[:1] + header[start:end]
        current_table_data = [row[:1] + row[start:end] for row in table_data]
        print(tabulate(current_table_data, headers=current_header, tablefmt="grid"))

# Display the seat matrices in chunks to fit terminal width
for seat_type in seat_types:
    has_seats = any(
        any((seat_info["online"] + seat_info["offline"]) > 0 for seat_info in fare_matrices[seat_type][from_city].values())
        for from_city in stations
    )
    
    if has_seats:
        print(f"\n{'-'*50}")
        print(f"Seat Matrix Representation for Seat Type: {seat_type}")
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
        print_table_in_chunks(table_data, header, chunk_size=12)

print("\nOnly seat matrices with available seats have been displayed.")

# User input for the journey with menu option
def display_menu():
    print("\nMenu Options:")
    print("1. Check Availability")
    print("2. Exit")

def prompt_user():
    while True:
        display_menu()
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice == '1':
            origin = input("\nEnter the origin station: ").strip()
            destination = input("Enter the destination station: ").strip()
            return origin, destination
        elif choice == '2':
            return None, None
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.")

# Pathfinding algorithm to find the segmented routes
def find_routes(origin, destination, seat_type):
    queue = deque([(origin, [], 0)])
    visited = set()

    while queue:
        current_station, path, total_fare = queue.popleft()

        if current_station in visited:
            continue
        visited.add(current_station)

        if current_station == destination:
            return path, total_fare

        for next_station in stations:
            if next_station == current_station or stations.index(next_station) <= stations.index(current_station):
                continue

            seat_info = fare_matrices[seat_type][current_station].get(next_station)
            if seat_info and seat_info["online"] > 0:
                next_fare = float(seat_info["fare"])
                vat_amount = float(seat_info.get("vat_amount", 0))
                total_cost = next_fare + vat_amount
                new_path = path + [(current_station, next_station, f"{next_fare} (Base) + {vat_amount} (VAT) = {total_cost}")]
                queue.append((next_station, new_path, total_fare + total_cost))

    return None

# Main interactive loop
while True:
    origin, destination = prompt_user()
    if origin is None or destination is None:
        print(f"\n{Fore.CYAN}Exiting the program. Thank you!")
        break

    # Display segmented routes only for seat types that have available seats
    for seat_type in seat_types:
        # Check if there is any segment in the seat matrix with available seats for the seat type
        has_available_seats = any(
            (fare_info["online"] + fare_info["offline"]) > 0
            for from_station in stations
            for to_station, fare_info in fare_matrices[seat_type][from_station].items()
            if from_station != to_station and stations.index(from_station) < stations.index(to_station)
        )

        if not has_available_seats:
            continue  # Skip seat types with no available seats

        # Check if the direct route is available
        direct_route_info = fare_matrices[seat_type][origin].get(destination)
        if direct_route_info and direct_route_info.get("online", 0) > 0:
            fare = float(direct_route_info["fare"])
            vat_amount = float(direct_route_info.get("vat_amount", 0))
            total_cost = fare + vat_amount

            print(f"\n{Fore.CYAN}Finding segmented route for seat type: {seat_type}")
            print(f"\n{Fore.GREEN}Direct route available for seat type {seat_type} from {origin} to {destination}.")
            print(f"Fare (Base): {fare} + VAT: {vat_amount} = Total Cost: {total_cost}")
        else:
            print(f"\n{Fore.CYAN}Finding segmented route for seat type: {seat_type}")
            result = find_routes(origin, destination, seat_type)
            if result:
                route_segments, total_fare = result
                print(f"{Fore.GREEN}Segmented route found for seat type {seat_type}:")
                for seg in route_segments:
                    print(f" - {seg[0]} to {seg[1]}, Fare + VAT: {seg[2]}")
                print(f"Total Fare: {total_fare}")
            else:
                print(f"{Fore.YELLOW}No segmented route available for seat type {seat_type}.")

    print(f"\n{Fore.CYAN}You can select an option from the menu again.")