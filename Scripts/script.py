import json
import csv
import tkinter as tk
from tkinter import filedialog

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle single dictionary by wrapping in a list
    if isinstance(data, dict):
        data = [data]
    
    # Collect fieldnames in order of first appearance
    fieldnames = []
    for entry in data:
        for key in entry:
            if key not in fieldnames:
                fieldnames.append(key)
    
    # Write CSV with columns in first-appearance order
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in data:
            # Fill missing keys with empty string to maintain column order
            writer.writerow({key: row.get(key, '') for key in fieldnames})

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    entry_input.delete(0, tk.END)
    entry_input.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    entry_output.delete(0, tk.END)
    entry_output.insert(0, file_path)

def convert():
    json_file = entry_input.get()
    csv_file = entry_output.get()
    if json_file and csv_file:
        try:
            json_to_csv(json_file, csv_file)
            lbl_status.config(text="Conversion Successful!")
        except Exception as e:
            lbl_status.config(text=f"Error: {str(e)}")
    else:
        lbl_status.config(text="Please select both file paths.")

# GUI setup remains the same
root = tk.Tk()
root.title("JSON to CSV Converter")

tk.Label(root, text="Input JSON File:").grid(row=0, column=0, padx=5, pady=5)
entry_input = tk.Entry(root, width=50)
entry_input.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output CSV File:").grid(row=1, column=0, padx=5, pady=5)
entry_output = tk.Entry(root, width=50)
entry_output.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=5, pady=5)

tk.Button(root, text="Convert", command=convert).grid(row=2, column=1, pady=10)

lbl_status = tk.Label(root, text="")
lbl_status.grid(row=3, column=1, pady=5)

root.mainloop()