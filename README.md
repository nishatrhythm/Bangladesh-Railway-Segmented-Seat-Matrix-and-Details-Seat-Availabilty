# Bangladesh Railway Segmented Fare Matrix

This project provides a solution to visualize and analyze train fare matrices for different seat types on specific train routes in Bangladesh. It features a script that fetches seat availability from a public API and constructs segmented travel routes when direct routes are not available. Ideal for travelers and developers, this tool offers detailed fare information, including VAT.

## Features

- **Real-Time Data Fetching**: Retrieves seat availability for different train routes and seat types.
- **Fare Matrix Display**: Presents fare matrices for each seat type in a tabular format.
- **Segmented Route Finder**: Calculates and displays alternative travel paths if a direct route is unavailable.
- **Detailed Fare Breakdown**: Shows base fare and VAT amounts for direct and segmented routes.
- **Interactive User Interface**: Menu-driven prompts for ease of use.

## Sample Run

Below is an example of the script running in the terminal:

![Script running in terminal](https://github.com/nishatrhythm/Bangladesh-Railway-Segmented-Fare-Matrix/blob/main/images/Screenshot_1.png)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nishatrhythm/Bangladesh-Railway-Segmented-Fare-Matrix.git
   cd Bangladesh-Railway-Segmented-Fare-Matrix
   ```
2. **Install required Python packages:** Ensure you have the required Python packages installed:
   ```bash
   pip install requests tabulate colorama
   ```

## Usage

1. **Modify the script:**
   - You need to update the `target_train_model` and `date_of_journey` variables in the `fareMatrixWithSegmentation.py` script to match your desired train model and date.
2. **Run the script:**
   ```bash
   python fareMatrixWithSegmentation.py
   ```
3. **Menu Options:**
   - Select **1** to check seat availability and enter origin and destination stations.
   - Select **2** to exit the program.
4. **Output Details:**
   - Displays fare matrices for each seat type if seats are available.
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
