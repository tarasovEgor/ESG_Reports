import os

folder_path = "PDF_processing_module/ESG-master/final"

for filename in os.listdir(folder_path):
    new_filename = filename.replace("$", "_")
    if new_filename != filename:
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)
        print(f'Renamed: {filename} -> {new_filename}')

print("Renaming completed.")