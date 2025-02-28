# import pandas as pd
# df = pd.read_json(r"raw/electricity_raw_data/hourly_demand_2022-01-01.json")
# df_normalized = pd.json_normalize(df["response"]["data"])
# df_normalized.to_csv(r"Outputs/Second34.csv", index=False)


# import os
# import json
# import pandas as pd
# import glob

# # Set the input and output directories
# input_folder = r"raw/electricity_raw_data"
# output_folder = r"Outputs/csvs"

# # Create the output folder if it doesn't exist
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # Find all JSON files in the input folder
# json_files = glob.glob(os.path.join(input_folder, "*.json"))

# # Loop over each JSON file
# for json_file in json_files:
#     with open(json_file, "r") as f:
#         data = json.load(f)
    
#     # Extract the records under the nested "response" -> "data"
#     records = data["response"]["data"]
    
#     # Normalize the records to a flat table
#     df = pd.json_normalize(records)
    
#     # Create an output filename based on the JSON file name
#     base_name = os.path.basename(json_file)
#     file_name = os.path.splitext(base_name)[0]
#     output_file = os.path.join(output_folder, file_name + ".csv")
    
#     # Save the DataFrame as a CSV file without the index column
#     df.to_csv(output_file, index=False)
#     print(f"Converted {json_file} to {output_file}")


# import os
# import json
# import pandas as pd
# import glob

# def convert_json_to_csv():
#     # Prompt user for input and output folders for JSON conversion
#     input_folder = input("Enter the path for the JSON files folder (e.g., raw/electricity_raw_data): ").strip()
#     output_folder = input("Enter the path for the output CSV folder (e.g., Outputs/csvs): ").strip()

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     # Find all JSON files in the input folder
#     json_files = glob.glob(os.path.join(input_folder, "*.json"))
    
#     if not json_files:
#         print("No JSON files found in the folder.")
#         return

#     for json_file in json_files:
#         try:
#             with open(json_file, "r") as f:
#                 data = json.load(f)
            
#             # Extract the records under the nested "response" -> "data"
#             records = data["response"]["data"]
            
#             # Normalize the records to a flat table
#             df = pd.json_normalize(records)
            
#             # Create an output filename based on the JSON file name
#             base_name = os.path.basename(json_file)
#             file_name = os.path.splitext(base_name)[0]
#             output_file = os.path.join(output_folder, file_name + ".csv")
            
#             # Save the DataFrame as a CSV file without the index column
#             df.to_csv(output_file, index=False)
#             print(f"Converted {json_file} to {output_file}")
#         except Exception as e:
#             print(f"Error processing {json_file}: {e}")

# def merge_csv_files():
#     # Prompt user for the two folders containing CSV files
#     folder1 = input("Enter the path for the first CSV folder: ").strip()
#     folder2 = input("Enter the path for the second CSV folder: ").strip()
    
#     # Find CSV files in both folders
#     csv_files1 = glob.glob(os.path.join(folder1, "*.csv"))
#     csv_files2 = glob.glob(os.path.join(folder2, "*.csv"))
#     all_csv_files = csv_files1 + csv_files2
    
#     if not all_csv_files:
#         print("No CSV files found in the provided folders.")
#         return
    
#     # Read each CSV file and collect the DataFrames
#     dfs = []
#     for csv_file in all_csv_files:
#         try:
#             df = pd.read_csv(csv_file)
#             dfs.append(df)
#             print(f"Loaded {csv_file}")
#         except Exception as e:
#             print(f"Error reading {csv_file}: {e}")
    
#     if dfs:
#         # Merge all DataFrames into one
#         merged_df = pd.concat(dfs, ignore_index=True)
#         # Save to a summary CSV in the current working directory
#         summary_file = os.path.join(os.getcwd(), "summary.csv")
#         merged_df.to_csv(summary_file, index=False)
#         print(f"Merged CSV saved as {summary_file}")
#     else:
#         print("No data to merge.")

# def main():
#     print("Select an option:")
#     print("1: Convert JSON files to CSV files")
#     print("2: Merge CSV files from two folders into summary.csv")
    
#     choice = input("Enter your choice (1 or 2): ").strip()
    
#     if choice == "1":
#         convert_json_to_csv()
#     elif choice == "2":
#         merge_csv_files()
#     else:
#         print("Invalid choice. Please run the script again and choose 1 or 2.")

# if __name__ == "__main__":
#     main()









# //////////////////////////////////////////////////////////////////////

# import os
# import json
# import pandas as pd
# import glob

# def convert_json_to_csv():
#     # Prompt user for input and output folders for JSON conversion
#     input_folder = input("Enter the path for the JSON files folder (e.g., raw/electricity_raw_data): ").strip().strip('"')
#     output_folder = input("Enter the path for the output CSV folder (e.g., Outputs/csvs): ").strip().strip('"')

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     # Find all JSON files in the input folder
#     json_files = glob.glob(os.path.join(input_folder, "*.json"))
    
#     if not json_files:
#         print("No JSON files found in the folder.")
#         return

#     for json_file in json_files:
#         try:
#             with open(json_file, "r") as f:
#                 data = json.load(f)
            
#             # Extract the records under the nested "response" -> "data"
#             records = data["response"]["data"]
            
#             # Normalize the records to a flat table
#             df = pd.json_normalize(records)
            
#             # Create an output filename based on the JSON file name
#             base_name = os.path.basename(json_file)
#             file_name = os.path.splitext(base_name)[0]
#             output_file = os.path.join(output_folder, file_name + ".csv")
            
#             # Save the DataFrame as a CSV file without the index column
#             df.to_csv(output_file, index=False)
#             print(f"Converted {json_file} to {output_file}")
#         except Exception as e:
#             print(f"Error processing {json_file}: {e}")

# def merge_csv_files():
#     # Prompt user for the two folders containing CSV files
#     folder1 = input("Enter the path for the first CSV folder: ").strip().strip('"')
#     folder2 = input("Enter the path for the second CSV folder: ").strip().strip('"')
    
#     # Get CSV files from each folder
#     csv_files1 = glob.glob(os.path.join(folder1, "*.csv"))
#     csv_files2 = glob.glob(os.path.join(folder2, "*.csv"))
    
#     if not csv_files1:
#         print("No CSV files found in folder1.")
#         return
#     if not csv_files2:
#         print("No CSV files found in folder2.")
#         return

#     # Merge all CSVs from folder1 vertically
#     dfs1 = []
#     for csv_file in csv_files1:
#         try:
#             df = pd.read_csv(csv_file)
#             dfs1.append(df)
#             print(f"Loaded {csv_file} from folder1")
#         except Exception as e:
#             print(f"Error reading {csv_file} from folder1: {e}")
#     if dfs1:
#         df1 = pd.concat(dfs1, ignore_index=True, sort=False).reset_index(drop=True)
#     else:
#         print("No data from folder1 to merge.")
#         return

#     # Merge all CSVs from folder2 vertically
#     dfs2 = []
#     for csv_file in csv_files2:
#         try:
#             df = pd.read_csv(csv_file)
#             dfs2.append(df)
#             print(f"Loaded {csv_file} from folder2")
#         except Exception as e:
#             print(f"Error reading {csv_file} from folder2: {e}")
#     if dfs2:
#         df2 = pd.concat(dfs2, ignore_index=True, sort=False).reset_index(drop=True)
#     else:
#         print("No data from folder2 to merge.")
#         return

#     # Now merge horizontally by aligning rows (i.e., first row of folder1 with first row of folder2, etc.)
#     merged_df = pd.concat([df1, df2], axis=1)
    
#     # Save the merged DataFrame to summary.csv in the current working directory
#     summary_file = os.path.join(os.getcwd(), "summary.csv")
#     try:
#         merged_df.to_csv(summary_file, index=False)
#         print(f"Merged CSV saved as {summary_file}")
#     except Exception as e:
#         print(f"Error saving merged CSV: {e}")

# def main():
#     print("Select an option:")
#     print("1: Convert JSON files to CSV files")
#     print("2: Merge CSV files from two folders into summary.csv")
    
#     choice = input("Enter your choice (1 or 2): ").strip()
    
#     if choice == "1":
#         convert_json_to_csv()
#     elif choice == "2":
#         merge_csv_files()
#     else:
#         print("Invalid choice. Please run the script again and choose 1 or 2.")

# if __name__ == "__main__":
#     main()



# /////////////////////////////////////////////////////////////////////////

import os
import json
import pandas as pd
import glob

def convert_json_to_csv():
    # Prompt user for input and output folders for JSON conversion
    input_folder = input("Enter the path for the JSON files folder (e.g., raw/electricity_raw_data): ").strip().strip('"')
    output_folder = input("Enter the path for the output CSV folder (e.g., Outputs/csvs): ").strip().strip('"')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Find all JSON files in the input folder
    json_files = glob.glob(os.path.join(input_folder, "*.json"))
    
    if not json_files:
        print("No JSON files found in the folder.")
        return

    for json_file in json_files:
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
            
            # Extract the records under the nested "response" -> "data"
            records = data["response"]["data"]
            
            # Normalize the records to a flat table
            df = pd.json_normalize(records)
            
            # Create an output filename based on the JSON file name
            base_name = os.path.basename(json_file)
            file_name = os.path.splitext(base_name)[0]
            output_file = os.path.join(output_folder, file_name + ".csv")
            
            # Save the DataFrame as a CSV file without the index column
            df.to_csv(output_file, index=False)
            print(f"Converted {json_file} to {output_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

def merge_csv_files():
    # Prompt user for the two folders containing CSV files
    folder1 = input("Enter the path for the first CSV folder: ").strip().strip('"')
    folder2 = input("Enter the path for the second CSV folder: ").strip().strip('"')
    
    # Normalize the folder paths
    folder1 = os.path.normpath(folder1)
    folder2 = os.path.normpath(folder2)
    
    # Check if the folders exist
    if not os.path.isdir(folder1):
        print(f"Folder1 does not exist: {folder1}")
        return
    if not os.path.isdir(folder2):
        print(f"Folder2 does not exist: {folder2}")
        return
    
    # Search for CSV files (both lower and upper case)
    csv_files1 = glob.glob(os.path.join(folder1, "*.csv")) + glob.glob(os.path.join(folder1, "*.CSV"))
    csv_files2 = glob.glob(os.path.join(folder2, "*.csv")) + glob.glob(os.path.join(folder2, "*.CSV"))
    
    print(f"Found {len(csv_files1)} CSV file(s) in folder1: {folder1}")
    print(f"Found {len(csv_files2)} CSV file(s) in folder2: {folder2}")
    
    if not csv_files1:
        print("No CSV files found in folder1.")
        return
    if not csv_files2:
        print("No CSV files found in folder2.")
        return

    # Merge all CSVs from folder1 vertically
    dfs1 = []
    for csv_file in csv_files1:
        try:
            df = pd.read_csv(csv_file)
            dfs1.append(df)
            print(f"Loaded {csv_file} from folder1")
        except Exception as e:
            print(f"Error reading {csv_file} from folder1: {e}")
    if dfs1:
        df1 = pd.concat(dfs1, ignore_index=True, sort=False).reset_index(drop=True)
    else:
        print("No data from folder1 to merge.")
        return

    # Merge all CSVs from folder2 vertically
    dfs2 = []
    for csv_file in csv_files2:
        try:
            df = pd.read_csv(csv_file)
            dfs2.append(df)
            print(f"Loaded {csv_file} from folder2")
        except Exception as e:
            print(f"Error reading {csv_file} from folder2: {e}")
    if dfs2:
        df2 = pd.concat(dfs2, ignore_index=True, sort=False).reset_index(drop=True)
    else:
        print("No data from folder2 to merge.")
        return

    # Now merge horizontally by aligning rows (i.e., first row of folder1 with first row of folder2, etc.)
    merged_df = pd.concat([df1, df2], axis=1)
    
    # Save the merged DataFrame to summary.csv in the current working directory
    summary_file = os.path.join(os.getcwd(), "summary.csv")
    try:
        merged_df.to_csv(summary_file, index=False)
        print(f"Merged CSV saved as {summary_file}")
    except Exception as e:
        print(f"Error saving merged CSV: {e}")

def main():
    print("Select an option:")
    print("1: Convert JSON files to CSV files")
    print("2: Merge CSV files from two folders into summary.csv")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        convert_json_to_csv()
    elif choice == "2":
        merge_csv_files()
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")

if __name__ == "__main__":
    main()
