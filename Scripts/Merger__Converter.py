import os
import json
import glob
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

def convert_json_to_csv(input_folder, output_folder):
    messages = []
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        messages.append(f"Created output folder: {output_folder}")
    
    json_files = glob.glob(os.path.join(input_folder, "*.json"))
    
    if not json_files:
        messages.append("No JSON files found in the folder.")
        return messages
    
    for json_file in json_files:
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
            records = data["response"]["data"]
            df = pd.json_normalize(records)
            
            base_name = os.path.basename(json_file)
            file_name = os.path.splitext(base_name)[0]
            output_file = os.path.join(output_folder, file_name + ".csv")
            
            df.to_csv(output_file, index=False)
            messages.append(f"Converted {json_file} to {output_file}")
        except Exception as e:
            messages.append(f"Error processing {json_file}: {e}")
    
    return messages

def merge_csv_files(folder1, folder2, output_file):
    messages = []
    
    # Get CSV files from each folder
    csv_files1 = glob.glob(os.path.join(folder1, "*.csv"))
    csv_files2 = glob.glob(os.path.join(folder2, "*.csv"))
    messages.append(f"Found {len(csv_files1)} CSV file(s) in folder1: {folder1}")
    messages.append(f"Found {len(csv_files2)} CSV file(s) in folder2: {folder2}")
    
    if not csv_files1:
        messages.append("No CSV files found in folder1.")
        return messages
    if not csv_files2:
        messages.append("No CSV files found in folder2.")
        return messages
    
    # Merge all CSVs from folder1 vertically
    dfs1 = []
    for csv_file in csv_files1:
        try:
            df = pd.read_csv(csv_file)
            dfs1.append(df)
            messages.append(f"Loaded {csv_file} (folder1)")
        except Exception as e:
            messages.append(f"Error reading {csv_file} (folder1): {e}")
    if dfs1:
        df1 = pd.concat(dfs1, ignore_index=True, sort=False)
        df1 = df1.reset_index(drop=True)
    else:
        messages.append("No data from folder1 to merge.")
        return messages
    
    # Merge all CSVs from folder2 vertically
    dfs2 = []
    for csv_file in csv_files2:
        try:
            df = pd.read_csv(csv_file)
            dfs2.append(df)
            messages.append(f"Loaded {csv_file} (folder2)")
        except Exception as e:
            messages.append(f"Error reading {csv_file} (folder2): {e}")
    if dfs2:
        df2 = pd.concat(dfs2, ignore_index=True, sort=False)
        df2 = df2.reset_index(drop=True)
    else:
        messages.append("No data from folder2 to merge.")
        return messages
    
    # Now merge horizontally (align rows by index)
    merged_df = pd.concat([df1, df2], axis=1)
    try:
        merged_df.to_csv(output_file, index=False)
        messages.append(f"Merged CSV saved as {output_file}")
    except Exception as e:
        messages.append(f"Error saving merged CSV: {e}")
    
    return messages

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Processor")
        self.geometry("400x200")
        self.resizable(False, False)
        
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))
        
        frame = ttk.Frame(self, padding="20")
        frame.pack(expand=True, fill="both")
        
        label = ttk.Label(frame, text="Select an Option:")
        label.pack(pady=10)
        
        btn1 = ttk.Button(frame, text="Convert JSON to CSV", command=self.open_json_converter)
        btn1.pack(pady=5, fill="x")
        
        btn2 = ttk.Button(frame, text="Merge CSV Files", command=self.open_csv_merger)
        btn2.pack(pady=5, fill="x")
    
    def open_json_converter(self):
        self.destroy()  # Close main window after option selection
        JsonConverterWindow()
    
    def open_csv_merger(self):
        self.destroy()  # Close main window after option selection
        CsvMergerWindow()

class JsonConverterWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON to CSV Converter")
        self.geometry("650x450")
        self.resizable(False, False)
        
        self.columnconfigure(1, weight=1)
        
        ttk.Label(self, text="Input Folder (JSON):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_folder = tk.StringVar()
        entry_input = ttk.Entry(self, textvariable=self.input_folder, width=50)
        entry_input.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        ttk.Button(self, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=10, pady=10)
        
        ttk.Label(self, text="Output Folder (CSV):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.output_folder = tk.StringVar()
        entry_output = ttk.Entry(self, textvariable=self.output_folder, width=50)
        entry_output.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        ttk.Button(self, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=10, pady=10)
        
        ttk.Button(self, text="Convert", command=self.convert).grid(row=2, column=1, pady=15)
        
        self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 10))
        self.log_area.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()
    
    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder (JSON)")
        if folder:
            self.input_folder.set(folder)
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder (CSV)")
        if folder:
            self.output_folder.set(folder)
    
    def convert(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return
        
        self.log_area.delete('1.0', tk.END)
        messages = convert_json_to_csv(input_folder, output_folder)
        for msg in messages:
            self.log_area.insert(tk.END, msg + "\n")
        
        messagebox.showinfo("Conversion Complete", "Process completed. Check log for details.")
        self.destroy()  # Auto-close after conversion
    
    def on_close(self):
        self.destroy()

class CsvMergerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Merger")
        self.geometry("650x450")
        self.resizable(False, False)
        
        self.columnconfigure(1, weight=1)
        
        ttk.Label(self, text="First CSV Folder:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.folder1 = tk.StringVar()
        entry_folder1 = ttk.Entry(self, textvariable=self.folder1, width=50)
        entry_folder1.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        ttk.Button(self, text="Browse", command=lambda: self.browse_folder(self.folder1)).grid(row=0, column=2, padx=10, pady=10)
        
        ttk.Label(self, text="Second CSV Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.folder2 = tk.StringVar()
        entry_folder2 = ttk.Entry(self, textvariable=self.folder2, width=50)
        entry_folder2.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        ttk.Button(self, text="Browse", command=lambda: self.browse_folder(self.folder2)).grid(row=1, column=2, padx=10, pady=10)
        
        ttk.Label(self, text="Output Merged CSV:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.output_csv = tk.StringVar()
        entry_output = ttk.Entry(self, textvariable=self.output_csv, width=50)
        entry_output.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        ttk.Button(self, text="Browse", command=self.browse_output_file).grid(row=2, column=2, padx=10, pady=10)
        
        ttk.Button(self, text="Merge", command=self.merge).grid(row=3, column=1, pady=15)
        
        self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 10))
        self.log_area.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()
    
    def browse_folder(self, folder_var):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            folder_var.set(folder)
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Merged CSV As", defaultextension=".csv",
                                                   filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.output_csv.set(file_path)
    
    def merge(self):
        folder1 = self.folder1.get()
        folder2 = self.folder2.get()
        output_file = self.output_csv.get()
        if not folder1 or not folder2 or not output_file:
            messagebox.showerror("Error", "Please select both folders and the output file.")
            return
        
        self.log_area.delete('1.0', tk.END)
        messages = merge_csv_files(folder1, folder2, output_file)
        for msg in messages:
            self.log_area.insert(tk.END, msg + "\n")
        
        messagebox.showinfo("Merge Complete", "Merge completed. Check log for details.")
        self.destroy()  # Auto-close after merge
    
    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
