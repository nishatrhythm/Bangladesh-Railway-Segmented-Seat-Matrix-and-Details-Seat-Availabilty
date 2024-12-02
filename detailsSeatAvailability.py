import requests
from tabulate import tabulate
from colorama import Fore, Style, init
import textwrap

# Initialize colorama
init(autoreset=True)

# Define constants
TOKEN = 'your_token_here'     # change as you need

from_city = "Dhaka"     # change as you neeed
to_city = "Joydebpur"       # change as you neeed
date_of_journey = "03-Dec-2024"     # change as you neeed
seat_class = "S_CHAIR"      # no need to change

# Helper Functions
def wrap_text(text, width=50):
    """Wrap text for better table formatting."""
    return "\n".join(textwrap.wrap(text, width))

def group_by_prefix(seats):
    """Group seat numbers by their prefix and count each group."""
    groups = {}
    for seat in seats:
        prefix = seat.split("-")[0]
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append(seat)
    return {prefix: {"seats": group, "count": len(group)} for prefix, group in groups.items()}

def pluralize(count, singular="ticket", plural="tickets"):
    """Return singular or plural form based on count."""
    return singular if count == 1 else singular if count == 0 else plural

def get_seat_layout(trip_id, trip_route_id):
    """Fetch seat layout for a specific train and seat type."""
    url = "https://railspaapi.shohoz.com/v1.0/web/bookings/seat-layout"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"trip_id": trip_id, "trip_route_id": trip_route_id}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        seat_layout = data.get("data", {}).get("seatLayout", [])
        
        # Separate seats into categories
        available_seats = []
        booking_process_seats = []

        for layout in seat_layout:
            for row in layout["layout"]:
                for seat in row:
                    if seat["seat_availability"] == 1:  # Available for booking
                        available_seats.append(seat["seat_number"])
                    elif seat["seat_availability"] == 2:  # In booking process
                        booking_process_seats.append(seat["seat_number"])
        
        # Group seats by prefix
        available_groups = group_by_prefix(available_seats)
        booking_process_groups = group_by_prefix(booking_process_seats)
        
        return available_groups, booking_process_groups, len(available_seats), len(booking_process_seats)
    else:
        print(f"{Fore.RED}Failed to fetch seat layout for trip_id: {trip_id}, trip_route_id: {trip_route_id}")
        print(Fore.RED + response.text)
        return {}, {}, 0, 0

# Main Script
url = "https://railspaapi.shohoz.com/v1.0/app/bookings/search-trips-v2"
headers = {"Authorization": f"Bearer {TOKEN}"}
payload = {
    "from_city": from_city,
    "to_city": to_city,
    "date_of_journey": date_of_journey,
    "seat_class": seat_class
}

# Fetch train details
response = requests.get(url, params=payload, headers=headers)

if response.status_code == 200:
    train_data = response.json().get("data", {}).get("trains", [])
    if not train_data:
        print(f"{Fore.YELLOW}No trains available for the given criteria.")
        exit()

    # Process each train
    for train in train_data:
        train_name = train["trip_number"]
        departure_time = train["departure_date_time"]
        arrival_time = train["arrival_date_time"]

        # Print train header
        print(f"\n{Fore.CYAN}{train_name} ({departure_time} - {arrival_time}) ({from_city} - {to_city}){Style.RESET_ALL}")
        print("=" * 80)

        for seat_type in train["seat_types"]:
            seat_type_name = seat_type["type"]
            trip_id = seat_type["trip_id"]
            trip_route_id = seat_type["trip_route_id"]

            # Fetch seat layout for the current seat type
            available_groups, booking_process_groups, available_count, booking_process_count = get_seat_layout(trip_id, trip_route_id)

            # Prepare table data
            table_data = []
            for prefix, data in available_groups.items():
                table_data.append([
                    Fore.GREEN + f"Available ({prefix}) - {data['count']} {pluralize(data['count'])}" + Style.RESET_ALL, 
                    wrap_text(", ".join(data["seats"]))
                ])
            for prefix, data in booking_process_groups.items():
                table_data.append([
                    Fore.YELLOW + f"In Booking Process ({prefix}) - {data['count']} {pluralize(data['count'])}" + Style.RESET_ALL, 
                    wrap_text(", ".join(data["seats"]))
                ])

            # Print table for this seat type
            if table_data:
                print(f"\nSeat Type: {Fore.MAGENTA}{seat_type_name}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Available Tickets: {available_count} {pluralize(available_count)} {Style.RESET_ALL}| {Fore.YELLOW}In Booking Process: {booking_process_count} {pluralize(booking_process_count)}")
                print(tabulate(table_data, headers=["Status", "Seat Numbers"], tablefmt="grid"))
            else:
                print(f"{Fore.YELLOW}No seat details available for seat type: {seat_type_name}")

else:
    print(f"{Fore.RED}Failed to fetch train details.")
    print(Fore.RED + response.text)