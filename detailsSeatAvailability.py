from typing import Dict, List, Tuple
import requests
from tabulate import tabulate
from colorama import Fore, Style, init
import textwrap

init(autoreset=True)

TOKEN = 'your_token_here'                # Replace with your authorization token
API_BASE_URL = 'https://railspaapi.shohoz.com/v1.0'
SEAT_AVAILABILITY = {'AVAILABLE': 1, 'IN_PROCESS': 2}

CONFIG = {
    'from_city': 'Dhaka',                # Set the origin city
    'to_city': 'Joydebpur',              # Set the destination city
    'date_of_journey': '03-Dec-2024',    # Set the date of journey
    'seat_class': 'S_CHAIR'              # No need to change this
}

def wrap_text(text: str, width: int = 50) -> str:
    return "\n".join(textwrap.wrap(text, width))

def group_by_prefix(seats: List[str]) -> Dict[str, dict]:
    groups: Dict[str, List[str]] = {}
    for seat in seats:
        prefix = seat.split("-")[0]
        groups.setdefault(prefix, []).append(seat)
    return {prefix: {"seats": group, "count": len(group)} for prefix, group in groups.items()}

def pluralize(count: int, singular: str = "ticket", plural: str = "tickets") -> str:
    return plural if count not in (0, 1) else singular

def get_seat_layout(trip_id: str, trip_route_id: str) -> Tuple[Dict, Dict, int, int]:
    url = f"{API_BASE_URL}/web/bookings/seat-layout"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"trip_id": trip_id, "trip_route_id": trip_route_id}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        seat_layout = data.get("data", {}).get("seatLayout", [])
        
        seats = [(seat["seat_number"], seat["seat_availability"], seat["ticket_type"]) 
                for layout in seat_layout 
                for row in layout["layout"] 
                for seat in row]
        
        available_seats = [num for num, avail, _ in seats if avail == SEAT_AVAILABILITY['AVAILABLE']]
        booking_process_seats = [num for num, avail, ttype in seats 
                                if avail == SEAT_AVAILABILITY['IN_PROCESS'] and ttype in {1, 2, 3}]
        
        return (group_by_prefix(available_seats),
                group_by_prefix(booking_process_seats),
                len(available_seats),
                len(booking_process_seats))
                
    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to fetch seat layout: {e}")
        return {}, {}, 0, 0

def main():
    url = f"{API_BASE_URL}/app/bookings/search-trips-v2"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    response = requests.get(url, params=CONFIG, headers=headers)
    if response.status_code != 200:
        print(f"{Fore.RED}Failed to fetch train details: {response.text}")
        return

    train_data = response.json().get("data", {}).get("trains", [])
    if not train_data:
        print(f"{Fore.YELLOW}No trains available for the given criteria.")
        return

    for train in train_data:
        print(f"\n{Fore.CYAN}{train['trip_number']} ({train['departure_date_time']} - {train['arrival_date_time']}) "
              f"({CONFIG['from_city']} - {CONFIG['to_city']}){Style.RESET_ALL}")
        print("=" * 80)
        
        for seat_type in train["seat_types"]:
            available_groups, booking_process_groups, available_count, booking_process_count = (
                get_seat_layout(seat_type["trip_id"], seat_type["trip_route_id"]))

            table_data = [
                *[
                    [f"{Fore.GREEN}Available ({prefix}) - {data['count']} {pluralize(data['count'])}{Style.RESET_ALL}",
                     wrap_text(", ".join(data["seats"]))]
                    for prefix, data in available_groups.items()
                ],
                *[
                    [f"{Fore.YELLOW}In Booking Process ({prefix}) - {data['count']} {pluralize(data['count'])}{Style.RESET_ALL}",
                     wrap_text(", ".join(data["seats"]))]
                    for prefix, data in booking_process_groups.items()
                ]
            ]

            if table_data:
                print(f"\nSeat Type: {Fore.MAGENTA}{seat_type['type']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Available Tickets: {available_count} {pluralize(available_count)} "
                      f"{Style.RESET_ALL}| {Fore.YELLOW}In Booking Process: {booking_process_count} "
                      f"{pluralize(booking_process_count)}")
                print(tabulate(table_data, headers=["Status", "Seat Numbers"], tablefmt="grid"))
            else:
                print(f"{Fore.YELLOW}No seat details available for seat type: {seat_type['type']}")

if __name__ == "__main__":
    main()
