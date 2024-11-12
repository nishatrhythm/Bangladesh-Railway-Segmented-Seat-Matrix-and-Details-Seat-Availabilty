import json
import os

# Directories for input and output
input_directory = 'train_responses'
output_directory = 'processed'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Function to process the JSON data
def process_json(data, model):
    if 'data' in data:
        # Add the train_model field
        data['data']['train_model'] = model
        
        # Remove the extra object if present
        if 'extra' in data:
            del data['extra']
        
        return data
    return None

# Process each JSON file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)
        
        # Extract train model from the filename (assuming it's at the end)
        model = filename.split('_')[-1].replace('.json', '')
        
        # Load and process the JSON data
        data = load_json(input_path)
        processed_data = process_json(data, model)
        
        if processed_data:
            # Save the processed data
            save_json(processed_data, output_path)
            print(f"Processed and saved: {output_path}")

print("All files have been processed and saved to the 'processed' directory.")