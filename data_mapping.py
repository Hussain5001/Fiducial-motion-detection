import os
import csv

# Paths
input_dir = "processed_data/individual_vids"  
output_mapping_file = "processed_data/mapping_data.csv"  

# Function to extract the target stack from file name
def extract_target_stack(file_name):
    try:

        parts = file_name.split("_")
        number_part = parts[-1].split(".")[0]  
        

        last_digit = int(str(number_part)[0])  
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

mapping_data = []

#walk through the individual video CSV directory
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".csv"):

            file_path = os.path.join(root, file)
            

            target_stack = extract_target_stack(file)
            
            mapping_data.append({
                "Video ID": file.replace(".csv", ""),
                "Target Stack": target_stack,
                "Input Data Path": file_path
            })

#write the mapping data to a CSV file
with open(output_mapping_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Video ID", "Target Stack", "Input Data Path"])
    writer.writeheader()
    writer.writerows(mapping_data)

print(f"Mapping file created: {output_mapping_file}")
