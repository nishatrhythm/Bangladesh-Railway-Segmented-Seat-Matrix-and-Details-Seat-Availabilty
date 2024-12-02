# Bangladesh Railway Segmented Seat Matrix and Details Seat Availabilty

This repository provides two powerful tools for visualizing and analyzing train seat availability in Bangladesh.

1. **[Segmented Seat Matrix](#segmented-seat-matrix)**  
    Visualize and analyze train seat matrices for different seat types on specific train routes in Bangladesh. It features scripts that fetch seat availability from a public API and **construct segmented travel routes when direct routes are not available**. This tool offers detailed seat information, including VAT.

2. **[Detailed Seat Availability](#detailed-seat-availability)**  
   Fetches and categorizes seat layouts into `Available` or `In Booking Process` groups, organizes seat numbers by prefixes for clarity, and uses color-coded output for enhanced readability.

## Segmented Seat Matrix

- **Real-Time Data Fetching**: Retrieves seat availability for different train routes and seat types.
- **Seat Matrix Display**: Presents seat matrices for each seat type in a tabular format.
- **Segmented Route Finder**: Calculates and displays alternative travel paths if a direct route is unavailable.
- **Detailed Fare Breakdown**: Shows base fare and VAT amounts for direct and segmented routes.
- **Interactive User Interface**: Menu-driven prompts for ease of use.

## Sample Run

Below is an example of the script running in the terminal:

![Script running in terminal](https://github.com/nishatrhythm/Bangladesh-Railway-Segmented-Seat-Matrix-and-Details-Seat-Availabilty/blob/main/images/Screenshot_1.png)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nishatrhythm/Bangladesh-Railway-Segmented-Seat-Matrix-and-Details-Seat-Availabilty.git
   cd Bangladesh-Railway-Segmented-Seat-Matrix-and-Details-Seat-Availabilty
   ```
2. **Install required Python packages:** Ensure you have the required Python packages installed:
   ```bash
   pip install requests tabulate colorama
   ```

## Usage

1. **Modify the script:**
   - You need to update the `target_train_model` and `date_of_journey` variables in the `seatMatrixWithSegmentation.py` script to match your desired train model and date.

   ```python
   target_train_model = "781"  # This can be set to match the desired train model
   date_of_journey = "15-Nov-2024"  # This can be modified as needed
   ```

2. **Run the script:**
   ```bash
   python seatMatrixWithSegmentation.py
   ```
3. **Menu Options:**
   - Select **1** to check seat availability and enter origin and destination stations.
   - Select **2** to exit the program.
4. **Output Details:**
   - Displays seat matrices for each seat type if seats are available.
   - Shows direct routes with a breakdown of base fare and VAT.
   - Finds and displays segmented routes if a direct route is not available.
  
### Example Output for a Route
   ```
   Finding segmented route for seat type: S_CHAIR
Segmented route found for seat type S_CHAIR:
 - Dhaka to Joydebpur, Fare (50.00) + VAT (7.50) = 57.50
 - Joydebpur to Mymensingh, Fare (100.00) + VAT (15.00) = 115.00
Total Fare: 172.50
   ```

## Detailed Seat Availability

### Features

- **Detailed Seat Layout**: Fetches and displays the seat layout, categorizing seats as available or in the booking process.
- **Grouped Seat Information**: Groups seat numbers by their prefixes for better clarity.
- **Color-Coded Output**: Utilizes colorama to color-code the output for enhanced readability.

## Sample Run

Below is an example of the script running in the terminal:

![Script running in terminal](https://github.com/nishatrhythm/Bangladesh-Railway-Segmented-Seat-Matrix-and-Details-Seat-Availabilty/blob/main/images/Screenshot_2.png)

### Installation

Ensure you have the following Python packages installed:

```bash
pip install requests tabulate colorama
```

## Usage

1. **Configure the Script:**

   Update the following variables in the `detailsSeatAvailability.py` script:
    
   ```python
   TOKEN = 'your_token_here'     # Replace with your authorization token
   from_city = "Dhaka"           # Set the origin city
   to_city = "Joydebpur"         # Set the destination city
   date_of_journey = "03-Dec-2024"  # Set the journey date
   ```

2. **Run the Script:**
   ```bash
   python detailsSeatAvailability.py
   ```

3. **Output Details:**
   - **Train Details**: Displays train name, departure, and arrival times for the selected route.
   - **Seat Availability**: Categorized by seat type, with seats grouped by prefixes for better organization.
    - **Color-Coded Table**: Indicates available seats and those in the booking process with visual distinctions for easy comprehension.

### Example Output
   ```
   TISTA EXPRESS (707) (03 Dec, 07:30 am - 03 Dec, 08:19 am) (Dhaka - Joydebpur)
   ================================================================================
    
   Seat Type: SNIGDHA
   Available Tickets: 0 ticket | In Booking Process: 2 tickets
   +-------------------------------------+----------------+
   | Status                              | Seat Numbers   |
   +=====================================+================+
   | In Booking Process (JA) - 2 tickets | JA-4, JA-19    |
   +-------------------------------------+----------------+
    
   Seat Type: S_CHAIR
   Available Tickets: 19 tickets | In Booking Process: 2 tickets
   +--------------------------------------+-------------------------------------------------+
   | Status                               | Seat Numbers                                    |
   +======================================+=================================================+
   | Available (THA) - 19 tickets         | THA-4, THA-6, THA-10, THA-12, THA-14, THA-17,   |
   |                                      | THA-18, THA-20, THA-23, THA-31, THA-32, THA-30, |
   |                                      | THA-29, THA-34, THA-36, THA-35, THA-39, THA-40, |
   |                                      | THA-38                                          |
   +--------------------------------------+-------------------------------------------------+
   | In Booking Process (NEO) - 2 tickets | NEO-55, NEO-56                                  |
   +--------------------------------------+-------------------------------------------------+
   No seat details available for seat type: AC_S
   ```
