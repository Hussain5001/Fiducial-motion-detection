import os
import csv

# Paths
input_dir = "processed_data/individual_vids"  # Path to individual CSV files
output_mapping_file = "processed_data/mapping_data.csv"  # Final mapping CSV file

# Function to extract the target stack from file name
def extract_target_stack(file_name):
    """
    Extract the target stack (stack1, stack2, stack3) from the file name.
    Example: 'sample_30_101.csv' -> 'stack1'
    """
    try:
        # Split file name to get the numeric part at the end
        parts = file_name.split("_")
        number_part = parts[-1].split(".")[0]  # Extract the '101' part
        
        # The last digit determines the stack
        last_digit = int(str(number_part)[0])  # Get the last digit
        if last_digit == 1:
            return "stack1"
        elif last_digit == 2:
            return "stack2"
        elif last_digit == 3:
            return "stack3"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error extracting target stack from {file_name}: {e}")
        return "unknown"

# List to store mapping data
mapping_data = []

# Walk through the individual video CSV directory
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".csv"):
            # Full path to the individual CSV file
            file_path = os.path.join(root, file)
            
            # Extract target stack
            target_stack = extract_target_stack(file)
            
            # Add to mapping data
            mapping_data.append({
                "Video ID": file.replace(".csv", ""),
                "Target Stack": target_stack,
                "Input Data Path": file_path
            })

# Write the mapping data to a CSV file
with open(output_mapping_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Video ID", "Target Stack", "Input Data Path"])
    writer.writeheader()
    writer.writerows(mapping_data)

print(f"Mapping file created: {output_mapping_file}")
