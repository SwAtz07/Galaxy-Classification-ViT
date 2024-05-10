# Standard libraries for I/O operations
import os
import shutil
import zipfile

# Data manipulation with pandas
import pandas as pd

# Ensure you're in the correct working directory
os.chdir('/path/to/your/working/directory')  # Change to your working directory

# Ensure the required directories exist
data_folder = 'data'  # This will hold the dataset and other files
sorted_folder = 'sorted_data'
smooth_folder = os.path.join(sorted_folder, 'smooth')
disk_folder = os.path.join(sorted_folder, 'disk')

# Create directories if they don't exist
os.makedirs(data_folder, exist_ok=True)
os.makedirs(smooth_folder, exist_ok=True)
os.makedirs(disk_folder, exist_ok=True)

# Path to the dataset and other resources
csv_file = os.path.join(data_folder, 'galaxy_data.csv')  # Input CSV
output_csv = os.path.join(data_folder, 'output.csv')  # Output CSV
image_dir = os.path.join(data_folder, 'images_training_rev1')  # Images

# Read the CSV file
df = pd.read_csv(csv_file)

# Clean and transform the data as needed
df_cleaned = df.iloc[:, 0:4]
df_cleaned = df_cleaned.drop(columns=['star'])  # Remove star column
df1 = df_cleaned.drop(columns=['disk'])  # Drop disk column
df2 = df_cleaned.drop(columns=['smooth'])  # Drop smooth column

# Modify columns with binary values based on threshold
df2 = df2.applymap(lambda x: 1 if x > 0.9 else 0)  # Smooth
df3 = df3.applymap(lambda x: 1 if x > 0.9 else 0)  # Disk

# Merge dataframes to create a new DataFrame
df_new = df2.copy()
df_new['disk'] = df3['disk']

# Ensure no invalid rows (with both 0s or invalid sums)
df_new['sum'] = df_new['smooth'] + df_new['disk']
df_new = df_new[df_new['sum'] != 0]
df_new.drop(columns=['sum'], inplace=True)  # Remove the sum column

# Save the cleaned DataFrame as CSV
df_new.to_csv(output_csv, index=False)

# Split data according to CSV labels
for _, row in df_new.iterrows():
    image_id = row['id']
    smooth_label = row['smooth']
    disk_label = row['disk']

    # Check if smooth label is 1
    if smooth_label == 1:
        source_path = os.path.join(image_dir, f'{image_id}.jpg')
        destination_path = os.path.join(smooth_folder, f'{image_id}.jpg')
        shutil.move(source_path, destination_path)

    # Check if disk label is 1
    if disk_label == 1:
        source_path = os.path.join(image_dir, f'{image_id}.jpg')
        destination_path = os.path.join(disk_folder, f'{image_id}.jpg')
        shutil.move(source_path, destination_path)

# Count files in a given directory
def count_files(directory):
    total_files = 0
    for root, _, files in os.walk(directory):
        total_files += len(files)
    return total_files

# Count files in smooth and disk directories
print("Total number of files in smooth:", count_files(smooth_folder))
print("Total number of files in disk:", count_files(disk_folder))

# Compress the sorted_data directory
folder_to_compress = sorted_folder
output_zip_path = os.path.join(data_folder, 'sorted_data.zip')

with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(folder_to_compress):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, folder_to_compress))

print("Folder compressed successfully.")
