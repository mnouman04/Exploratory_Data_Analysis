# import os
# import pandas as pd
# import numpy as np
# from datetime import datetime

# # ------------------------------------------------------------------------------
# # Helper function: Determine season from month
# # ------------------------------------------------------------------------------
# def get_season(month):
#     """
#     Given a month (as an integer), return the corresponding season.
#     Winter: Dec, Jan, Feb; Spring: Mar, Apr, May; Summer: Jun, Jul, Aug; Fall: Sep, Oct, Nov.
#     """
#     if month in [12, 1, 2]:
#         return "Winter"
#     elif month in [3, 4, 5]:
#         return "Spring"
#     elif month in [6, 7, 8]:
#         return "Summer"
#     else:
#         return "Fall"

# # ------------------------------------------------------------------------------
# # Main cleaning function
# # ------------------------------------------------------------------------------
# def clean_data(df):
#     """
#     Clean and preprocess the DataFrame.
    
#     Steps:
    
#     1. Missing Data & Imputation:
#        - Replace empty strings with NaN.
#        - For numeric columns (except 'temperature_2m'), impute missing values with the median.
#        - For categorical columns, impute missing values with the mode.
       
#     2. Data Type Conversions & Temporal Feature Extraction:
#        - Convert columns with names 'period' or 'date', or containing 'date'/'time', to datetime.
#        - Extract additional temporal features from these columns, storing them with prefix "extracted_".
#          (For example, for a column "date", new columns "extracted_date_hour", "extracted_date_day", etc. are created.)
       
#     3. Handling Duplicates and Constant Columns:
#        - Remove duplicate rows.
#        - Drop columns that contain only one unique value.
       
#     4. Outlier Handling:
#        - For numeric columns (except 'temperature_2m'), remove outliers using the 1.5*IQR rule.
#        - For 'temperature_2m', if it is variable, mark outliers in a new column "temperature_anomaly"
#          and sort so that normal values appear first.
       
#     5. Feature Engineering:
#        - Standardize numeric columns (z-score normalization) and add new columns with the suffix "_std".
       
#     Returns:
#         The cleaned DataFrame.
#     """
#     # --- Step 0: Replace empty strings with NaN ---
#     df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
#     # --- Step 1: Missing Data & Imputation ---
#     print("Missing data percentage per column:")
#     missing_pct = df.isna().mean() * 100
#     print(missing_pct)
    
#     # Identify numeric and categorical columns
#     numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
#     categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
#     # Impute numeric columns (excluding 'temperature_2m') with the median
#     for col in numeric_cols:
#         if col != "temperature_2m" and df[col].isna().sum() > 0:
#             median_val = df[col].median()
#             df[col] = df[col].fillna(median_val)
#             print(f"Imputed missing values in numeric column '{col}' with median: {median_val}")
    
#     # Impute categorical columns with the mode
#     for col in categorical_cols:
#         if df[col].isna().sum() > 0:
#             mode_val = df[col].mode()[0]
#             df[col] = df[col].fillna(mode_val)
#             print(f"Imputed missing values in categorical column '{col}' with mode: {mode_val}")
    
#     # --- Step 2: Data Type Conversions & Temporal Feature Extraction ---
#     # Convert columns likely to be dates to datetime and extract features with a prefix
#     for col in df.columns:
#         if col.lower() in ['period', 'date'] or ("date" in col.lower() or "time" in col.lower()):
#             try:
#                 df[col] = pd.to_datetime(df[col], errors='coerce')
#                 print(f"Converted column '{col}' to datetime.")
#                 if df[col].notna().sum() > 0:
#                     # Use a prefix "extracted_" so original column header remains unchanged
#                     df["extracted_" + col + "_hour"] = df[col].dt.hour
#                     df["extracted_" + col + "_day"] = df[col].dt.day
#                     df["extracted_" + col + "_month"] = df[col].dt.month
#                     df["extracted_" + col + "_dayofweek"] = df[col].dt.dayofweek
#                     df["extracted_" + col + "_is_weekend"] = df[col].dt.dayofweek >= 5
#                     df["extracted_" + col + "_season"] = df[col].dt.month.apply(get_season)
#             except Exception as e:
#                 print(f"Could not convert column '{col}' to datetime: {e}")
    
#     # --- Step 3: Handling Duplicates and Constant Columns ---
#     initial_rows = df.shape[0]
#     df.drop_duplicates(inplace=True)
#     duplicates_removed = initial_rows - df.shape[0]
#     if duplicates_removed > 0:
#         print(f"Removed {duplicates_removed} duplicate rows.")
    
#     constant_columns = [col for col in df.columns if df[col].nunique() <= 1]
#     if constant_columns:
#         df.drop(columns=constant_columns, inplace=True)
#         print(f"Dropped constant columns: {constant_columns}")
    
#     # --- Step 4: Outlier Handling ---
#     # For numeric columns (except 'temperature_2m'), remove outliers using the 1.5*IQR rule.
#     for col in numeric_cols:
#         if col in df.columns and col != "temperature_2m":
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
#             lower_bound = Q1 - 1.5 * IQR
#             upper_bound = Q3 + 1.5 * IQR
#             before_rows = df.shape[0]
#             df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
#             after_rows = df.shape[0]
#             if before_rows != after_rows:
#                 print(f"Removed {before_rows - after_rows} outliers from column '{col}'.")
    
#     # For 'temperature_2m', mark anomalies if the column is variable.
#     if "temperature_2m" in df.columns:
#         if df["temperature_2m"].nunique() > 1:
#             Q1 = df["temperature_2m"].quantile(0.25)
#             Q3 = df["temperature_2m"].quantile(0.75)
#             IQR = Q3 - Q1
#             lower_bound = Q1 - 1.5 * IQR
#             upper_bound = Q3 + 1.5 * IQR
#             df["temperature_anomaly"] = ~df["temperature_2m"].between(lower_bound, upper_bound)
#             n_anomalies = df["temperature_anomaly"].sum()
#             print(f"Marked {n_anomalies} anomalies in 'temperature_2m'.")
#             df = df.sort_values(by="temperature_anomaly", ascending=True).reset_index(drop=True)
#         else:
#             print("Temperature column 'temperature_2m' is constant; no anomaly marking applied.")
    
#     # --- Step 5: Feature Engineering: Standardization ---
#     for col in numeric_cols:
#         if col in df.columns:
#             std_col = col + "_std"
#             df[std_col] = (df[col] - df[col].mean()) / df[col].std()
#             print(f"Created standardized feature '{std_col}'.")
    
#     return df

# # ------------------------------------------------------------------------------
# # Main function: Load, clean, and save CSV; generate summary statistics
# # ------------------------------------------------------------------------------
# def main():
#     # Prompt for input CSV file and output destination
#     input_file = input("Enter the path for the input CSV file: ").strip().strip('"')
#     output_path = input("Enter the path for the cleaned output CSV file or folder: ").strip().strip('"')
    
#     # Verify input file exists
#     if not os.path.exists(input_file):
#         print(f"Input file does not exist: {input_file}")
#         return
    
#     # Determine output file path. If a folder is given, append a default filename.
#     if os.path.isdir(output_path):
#         output_file = os.path.join(output_path, "cleaned_output.csv")
#         stats_file = os.path.join(output_path, "cleaned_stats.txt")
#     else:
#         output_file = output_path
#         stats_file = os.path.splitext(output_file)[0] + "_stats.txt"
    
#     # Load the input CSV
#     try:
#         df = pd.read_csv(input_file)
#     except Exception as e:
#         print(f"Error reading CSV: {e}")
#         return
    
#     print(f"Original DataFrame shape: {df.shape}")
    
#     # Clean the data
#     cleaned_df = clean_data(df)
#     print(f"Cleaned DataFrame shape: {cleaned_df.shape}")
    
#     # Save the cleaned DataFrame
#     try:
#         cleaned_df.to_csv(output_file, index=False)
#         print(f"Cleaned CSV saved as {output_file}")
#     except Exception as e:
#         print(f"Error saving cleaned CSV: {e}")
    
#     # Generate summary statistics and save to a text file
#     try:
#         summary_stats = cleaned_df.describe(include='all')
#         summary_str = summary_stats.to_string()
#         with open(stats_file, "w") as f:
#             f.write("Summary Statistics for Cleaned Data\n")
#             f.write("=" * 50 + "\n\n")
#             f.write(summary_str)
#         print(f"Summary statistics saved as {stats_file}")
#     except Exception as e:
#         print(f"Error saving summary statistics: {e}")

# if __name__ == "__main__":
#     main()

# //////////////////////////

# import os
# import pandas as pd
# import numpy as np
# from datetime import datetime

# # ------------------------------------------------------------------------------
# # Helper function: Determine season from month
# # ------------------------------------------------------------------------------
# def get_season(month):
#     """
#     Given a month (as an integer), return the corresponding season.
#     Winter: Dec, Jan, Feb; Spring: Mar, Apr, May; Summer: Jun, Jul, Aug; Fall: Sep, Oct, Nov.
#     """
#     if month in [12, 1, 2]:
#         return "Winter"
#     elif month in [3, 4, 5]:
#         return "Spring"
#     elif month in [6, 7, 8]:
#         return "Summer"
#     else:
#         return "Fall"

# # ------------------------------------------------------------------------------
# # Main cleaning function
# # ------------------------------------------------------------------------------
# def clean_data(df):
#     """
#     Clean and preprocess the DataFrame.
    
#     1. Missing Data & Imputation:
#        - Replace empty strings with NaN.
#        - For numeric columns (except 'temperature_2m'), impute missing values with the median.
#        - For categorical columns, impute missing values with the mode.
    
#     2. Data Type Conversions & Temporal Feature Extraction:
#        - Convert columns whose name is 'date' or 'period' (or containing 'date'/'time')
#          to datetime.
#        - For each such column, if at least one valid date is found, extract features 
#          (hour, day, month, dayofweek, is_weekend, season) into new columns prefixed with "extracted_".
#        - If the extracted features contain missing values, impute them by randomly
#          assigning plausible values (e.g., hour: 0–23, day: 1–28, month: 1–12, dayofweek: 0–6).
#        - If the entire column is invalid (all NaT), fill it with random dates in 2020 and extract features.
    
#     3. Handling Duplicates & Constant Columns:
#        - Remove duplicate rows.
#        - Drop columns with only one unique value.
    
#     4. Outlier Handling:
#        - For numeric columns (except 'temperature_2m'), remove outliers using the 1.5*IQR rule.
#        - For 'temperature_2m', if variable, mark outliers in a new column "temperature_anomaly"
#          and sort so that normal values appear first.
    
#     5. Feature Engineering:
#        - Standardize numeric columns (z-score) and add new columns with '_std' suffix.
    
#     Returns:
#        The cleaned DataFrame.
#     """
    
#     # --- Step 0: Replace empty strings with NaN ---
#     df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
#     # --- Step 1: Missing Data & Imputation ---
#     print("Missing data percentage per column:")
#     missing_pct = df.isna().mean() * 100
#     print(missing_pct)
    
#     # Identify numeric and categorical columns
#     numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
#     categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
#     # Impute numeric columns (except 'temperature_2m') with the median
#     for col in numeric_cols:
#         if col != "temperature_2m" and df[col].isna().sum() > 0:
#             median_val = df[col].median()
#             df[col] = df[col].fillna(median_val)
#             print(f"Imputed missing values in numeric column '{col}' with median: {median_val}")
    
#     # Impute categorical columns with the mode
#     for col in categorical_cols:
#         if df[col].isna().sum() > 0:
#             mode_val = df[col].mode()[0]
#             df[col] = df[col].fillna(mode_val)
#             print(f"Imputed missing values in categorical column '{col}' with mode: {mode_val}")
    
#     # --- Step 2: Data Type Conversions & Temporal Feature Extraction ---
#     # For columns whose name is 'date' or 'period' or containing 'date'/'time', convert to datetime.
#     for col in df.columns:
#         if col.lower() in ['period', 'date'] or ("date" in col.lower() or "time" in col.lower()):
#             try:
#                 df[col] = pd.to_datetime(df[col], errors='coerce')
#                 print(f"Converted column '{col}' to datetime.")
                
#                 # Define prefix for extracted features; do not override original column.
#                 prefix = "extracted_" + col
                
#                 # If there are valid dates in the column, extract features.
#                 if df[col].notna().sum() > 0:
#                     df[prefix + "_hour"] = df[col].dt.hour
#                     df[prefix + "_day"] = df[col].dt.day
#                     df[prefix + "_month"] = df[col].dt.month
#                     df[prefix + "_dayofweek"] = df[col].dt.dayofweek
#                     df[prefix + "_is_weekend"] = df[col].dt.dayofweek >= 5
#                     df[prefix + "_season"] = df[col].dt.month.apply(get_season)
                    
#                     # Now, for each extracted feature, if there are still missing values, fill them randomly.
#                     n = df.shape[0]
#                     if df[prefix + "_hour"].isna().sum() > 0:
#                         df[prefix + "_hour"].fillna(pd.Series(np.random.randint(0, 24, size=n), index=df.index), inplace=True)
#                         print(f"Randomly imputed missing values in {prefix + '_hour'}.")
#                     if df[prefix + "_day"].isna().sum() > 0:
#                         df[prefix + "_day"].fillna(pd.Series(np.random.randint(1, 29, size=n), index=df.index), inplace=True)
#                         print(f"Randomly imputed missing values in {prefix + '_day'}.")
#                     if df[prefix + "_month"].isna().sum() > 0:
#                         df[prefix + "_month"].fillna(pd.Series(np.random.randint(1, 13, size=n), index=df.index), inplace=True)
#                         print(f"Randomly imputed missing values in {prefix + '_month'}.")
#                     if df[prefix + "_dayofweek"].isna().sum() > 0:
#                         df[prefix + "_dayofweek"].fillna(pd.Series(np.random.randint(0, 7, size=n), index=df.index), inplace=True)
#                         print(f"Randomly imputed missing values in {prefix + '_dayofweek'}.")
#                     # (is_weekend and season will be computed from the above; if missing, they can be recomputed)
#                     df[prefix + "_is_weekend"] = df[prefix + "_dayofweek"].apply(lambda x: x >= 5)
#                     df[prefix + "_season"] = df[prefix + "_month"].apply(get_season)
#                 else:
#                     # If entire column is invalid (all NaT), fill with random dates from a fixed range.
#                     print(f"Column '{col}' has no valid dates. Imputing with random dates in 2020.")
#                     random_dates = pd.to_datetime(np.random.choice(pd.date_range("2020-01-01", "2020-12-31"), size=df.shape[0]))
#                     df[col] = random_dates
#                     prefix = "extracted_" + col
#                     df[prefix + "_hour"] = df[col].dt.hour
#                     df[prefix + "_day"] = df[col].dt.day
#                     df[prefix + "_month"] = df[col].dt.month
#                     df[prefix + "_dayofweek"] = df[col].dt.dayofweek
#                     df[prefix + "_is_weekend"] = df[col].dt.dayofweek >= 5
#                     df[prefix + "_season"] = df[col].dt.month.apply(get_season)
#             except Exception as e:
#                 print(f"Could not convert column '{col}' to datetime: {e}")
    
#     # --- Step 3: Handling Duplicates and Constant Columns ---
#     initial_rows = df.shape[0]
#     df.drop_duplicates(inplace=True)
#     duplicates_removed = initial_rows - df.shape[0]
#     if duplicates_removed > 0:
#         print(f"Removed {duplicates_removed} duplicate rows.")
    
#     constant_columns = [col for col in df.columns if df[col].nunique() <= 1]
#     if constant_columns:
#         df.drop(columns=constant_columns, inplace=True)
#         print(f"Dropped constant columns: {constant_columns}")
    
#     # --- Step 4: Outlier Handling ---
#     # For numeric columns (except 'temperature_2m'), remove outliers using the 1.5*IQR rule.
#     for col in numeric_cols:
#         if col in df.columns and col != "temperature_2m":
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
#             lower_bound = Q1 - 1.5 * IQR
#             upper_bound = Q3 + 1.5 * IQR
#             before_rows = df.shape[0]
#             df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
#             after_rows = df.shape[0]
#             if before_rows != after_rows:
#                 print(f"Removed {before_rows - after_rows} outliers from column '{col}'.")
    
#     # For 'temperature_2m': if it has variability, mark anomalies rather than removing rows.
#     if "temperature_2m" in df.columns:
#         if df["temperature_2m"].nunique() > 1:
#             Q1 = df["temperature_2m"].quantile(0.25)
#             Q3 = df["temperature_2m"].quantile(0.75)
#             IQR = Q3 - Q1
#             lower_bound = Q1 - 1.5 * IQR
#             upper_bound = Q3 + 1.5 * IQR
#             df["temperature_anomaly"] = ~df["temperature_2m"].between(lower_bound, upper_bound)
#             n_anomalies = df["temperature_anomaly"].sum()
#             print(f"Marked {n_anomalies} anomalies in 'temperature_2m'.")
#             df = df.sort_values(by="temperature_anomaly", ascending=True).reset_index(drop=True)
#         else:
#             print("Temperature column 'temperature_2m' is constant; no anomaly marking applied.")
    
#     # --- Step 5: Feature Engineering: Standardization ---
#     for col in numeric_cols:
#         if col in df.columns:
#             std_col = col + "_std"
#             df[std_col] = (df[col] - df[col].mean()) / df[col].std()
#             print(f"Created standardized feature '{std_col}'.")
    
#     return df

# # ------------------------------------------------------------------------------
# # Main function: Load, clean, save CSV; generate summary statistics
# # ------------------------------------------------------------------------------
# def main():
#     # Prompt for input CSV file and output destination
#     input_file = input("Enter the path for the input CSV file: ").strip().strip('"')
#     output_path = input("Enter the path for the cleaned output CSV file or folder: ").strip().strip('"')
    
#     # Verify input file exists
#     if not os.path.exists(input_file):
#         print(f"Input file does not exist: {input_file}")
#         return
    
#     # Determine output file path. If a folder is given, append default filenames.
#     if os.path.isdir(output_path):
#         output_file = os.path.join(output_path, "cleaned_output.csv")
#         stats_file = os.path.join(output_path, "cleaned_stats.txt")
#     else:
#         output_file = output_path
#         stats_file = os.path.splitext(output_file)[0] + "_stats.txt"
    
#     # Load the input CSV
#     try:
#         df = pd.read_csv(input_file)
#     except Exception as e:
#         print(f"Error reading CSV: {e}")
#         return
    
#     print(f"Original DataFrame shape: {df.shape}")
    
#     # Clean the data
#     cleaned_df = clean_data(df)
#     print(f"Cleaned DataFrame shape: {cleaned_df.shape}")
    
#     # Save the cleaned DataFrame
#     try:
#         cleaned_df.to_csv(output_file, index=False)
#         print(f"Cleaned CSV saved as {output_file}")
#     except Exception as e:
#         print(f"Error saving cleaned CSV: {e}")
    
#     # Generate summary statistics and save to a text file
#     try:
#         summary_stats = cleaned_df.describe(include='all')
#         summary_str = summary_stats.to_string()
#         with open(stats_file, "w") as f:
#             f.write("Summary Statistics for Cleaned Data\n")
#             f.write("=" * 50 + "\n\n")
#             f.write(summary_str)
#         print(f"Summary statistics saved as {stats_file}")
#     except Exception as e:
#         print(f"Error saving summary statistics: {e}")

# if __name__ == "__main__":
#     main()

import os
import pandas as pd
import numpy as np
from datetime import datetime

# ------------------------------------------------------------------------------
# Helper function: Determine season from month
# ------------------------------------------------------------------------------
def get_season(month):
    """
    Given a month (as an integer), return the corresponding season.
    Winter: Dec, Jan, Feb; Spring: Mar, Apr, May; Summer: Jun, Jul, Aug; Fall: Sep, Oct, Nov.
    """
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

# ------------------------------------------------------------------------------
# Main cleaning function
# ------------------------------------------------------------------------------
def clean_data(df, log):
    """
    Clean and preprocess the DataFrame.
    
    1. Missing Data & Imputation:
       - Replace empty strings with NaN.
       - For numeric columns (except 'temperature_2m'), impute missing values with the median.
       - For categorical columns, impute missing values with the mode.
    
    2. Data Type Conversions & Temporal Feature Extraction:
       - For each column whose name is "date", "period", or contains "date" or "time":
           a. Convert the column to datetime (invalid entries become NaT).
           b. If any dates are missing but valid dates exist, impute them with the mode.
           c. Re-convert to datetime to ensure consistency.
           d. Extract features (hour, day, month, dayofweek) into new columns prefixed with "extracted_".
           e. If any extracted feature is still missing, impute it with the median of valid values.
           f. Compute derived features "extracted_<col>_is_weekend" and "extracted_<col>_season".
    
    3. Handling Duplicates & Constant Columns:
       - Remove duplicate rows.
       - Drop columns that contain only one unique value, except for the "value" column.
    
    4. Outlier Handling:
       - For each numeric column (except 'temperature_2m'), remove rows outside 1.5×IQR and record a summary.
       - For 'temperature_2m', mark anomalies in a new column "temperature_anomaly" (without removing rows).
    
    5. Feature Engineering:
       - Standardize numeric columns (z-score) into new columns with the suffix "_std".
       
    Returns:
       The cleaned DataFrame and a dictionary of outlier summaries.
    """
    
    # --- Step 0: Replace empty strings with NaN ---
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
    # --- Step 1: Missing Data & Imputation ---
    log.append("Missing data percentage per column:")
    missing_pct = df.isna().mean() * 100
    log.append(missing_pct.to_string())
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Impute numeric columns (except 'temperature_2m') with median
    for col in numeric_cols:
        if col != "temperature_2m" and df[col].isna().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            log.append(f"Imputed missing values in numeric column '{col}' with median: {median_val}")
    
    # Impute categorical columns with mode
    for col in categorical_cols:
        if df[col].isna().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            log.append(f"Imputed missing values in categorical column '{col}' with mode: {mode_val}")
    
    # --- Step 2: Data Type Conversions & Temporal Feature Extraction ---
    for col in df.columns:
        if col.lower() in ['period', 'date'] or ("date" in col.lower() or "time" in col.lower()):
            try:
                # First, convert to datetime (invalid values become NaT)
                df[col] = pd.to_datetime(df[col], errors='coerce')
                # If missing values exist and there are valid ones, impute using mode
                if df[col].isna().sum() > 0 and df[col].notna().sum() > 0:
                    mode_date = df[col].mode()[0]
                    df[col] = df[col].fillna(mode_date)
                    log.append(f"Imputed missing values in date column '{col}' with mode: {mode_date}")
                # Ensure the column is datetime
                df[col] = pd.to_datetime(df[col], errors='coerce')
                log.append(f"Converted column '{col}' to datetime.")
                
                # Extract temporal features with a prefix so original column is not overwritten
                prefix = "extracted_" + col
                if df[col].notna().sum() > 0:
                    df[prefix + "_hour"] = df[col].dt.hour
                    df[prefix + "_day"] = df[col].dt.day
                    df[prefix + "_month"] = df[col].dt.month
                    df[prefix + "_dayofweek"] = df[col].dt.dayofweek
                    # For any missing extracted values, impute with median of the valid ones
                    for feat, rng in [("_hour", (0,23)), ("_day", (1,28)), ("_month", (1,12)), ("_dayofweek", (0,6))]:
                        feat_col = prefix + feat
                        if df[feat_col].isna().sum() > 0 and df[feat_col].notna().sum() > 0:
                            median_val = int(round(df[feat_col].median()))
                            df[feat_col] = df[feat_col].fillna(median_val)
                            log.append(f"Imputed missing values in {feat_col} with median: {median_val}")
                    # Compute derived features from the imputed values
                    df[prefix + "_is_weekend"] = df[prefix + "_dayofweek"].apply(lambda x: x >= 5)
                    df[prefix + "_season"] = df[prefix + "_month"].apply(get_season)
                else:
                    log.append(f"Column '{col}' has no valid dates; no temporal features extracted.")
            except Exception as e:
                log.append(f"Error processing date column '{col}': {e}")
    
    # --- Step 3: Handling Duplicates & Constant Columns ---
    initial_rows = df.shape[0]
    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - df.shape[0]
    if duplicates_removed > 0:
        log.append(f"Removed {duplicates_removed} duplicate rows.")
    
    # Drop constant columns except for "value"
    constant_columns = [col for col in df.columns if df[col].nunique() <= 1 and col.lower() != "value"]
    if constant_columns:
        df.drop(columns=constant_columns, inplace=True)
        log.append(f"Dropped constant columns (excluding 'value'): {constant_columns}")
    
    # --- Step 4: Outlier Handling ---
    outlier_summary = {}
    for col in numeric_cols:
        if col in df.columns and col != "temperature_2m":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            before_rows = df.shape[0]
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            after_rows = df.shape[0]
            removed = before_rows - after_rows
            if removed > 0:
                outlier_summary[col] = f"Removed {removed} outliers"
                log.append(f"Removed {removed} outliers from column '{col}'.")
            else:
                outlier_summary[col] = "No outliers"
                log.append(f"No outliers found in column '{col}'.")
    
    # For 'temperature_2m', mark anomalies if variable.
    if "temperature_2m" in df.columns:
        if df["temperature_2m"].nunique() > 1:
            Q1 = df["temperature_2m"].quantile(0.25)
            Q3 = df["temperature_2m"].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df["temperature_anomaly"] = ~df["temperature_2m"].between(lower_bound, upper_bound)
            n_anomalies = df["temperature_anomaly"].sum()
            outlier_summary["temperature_2m"] = f"Marked {n_anomalies} anomalies"
            log.append(f"Marked {n_anomalies} anomalies in 'temperature_2m'.")
            df = df.sort_values(by="temperature_anomaly", ascending=True).reset_index(drop=True)
        else:
            outlier_summary["temperature_2m"] = "No outliers (constant)"
            log.append("Temperature column 'temperature_2m' is constant; no anomaly marking applied.")
    
    # --- Step 5: Feature Engineering: Standardization ---
    for col in numeric_cols:
        if col in df.columns:
            std_col = col + "_std"
            df[std_col] = (df[col] - df[col].mean()) / df[col].std()
            log.append(f"Created standardized feature '{std_col}'.")
    
    # Append outlier summary to log with heading
    log.append("\n***** Outlier Summary *****")
    for col, summary in outlier_summary.items():
        log.append(f"{col}: {summary}")
    
    return df, outlier_summary

# ------------------------------------------------------------------------------
# Main function: Load, clean, save CSV; generate summary statistics log
# ------------------------------------------------------------------------------
def main():
    log = []
    
    # Prompt for the input CSV file and output destination
    input_file = input("Enter the path for the input CSV file: ").strip().strip('"')
    output_path = input("Enter the path for the cleaned output CSV file or folder: ").strip().strip('"')
    
    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"Input file does not exist: {input_file}")
        return
    
    # Determine output file paths. If a folder is given, append default filenames.
    if os.path.isdir(output_path):
        output_file = os.path.join(output_path, "cleaned_output.csv")
        stats_file = os.path.join(output_path, "cleaned_stats.txt")
    else:
        output_file = output_path
        stats_file = os.path.splitext(output_file)[0] + "_stats.txt"
    
    # Load the input CSV
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    log.append(f"Original DataFrame shape: {df.shape}")
    
    # Clean the data
    cleaned_df, outlier_summary = clean_data(df, log)
    log.append(f"Cleaned DataFrame shape: {cleaned_df.shape}")
    
    # Save the cleaned DataFrame
    try:
        cleaned_df.to_csv(output_file, index=False)
        log.append(f"Cleaned CSV saved as {output_file}")
        print(f"Cleaned CSV saved as {output_file}")
    except Exception as e:
        log.append(f"Error saving cleaned CSV: {e}")
        print(f"Error saving cleaned CSV: {e}")
    
    # Generate summary statistics and write log to stats file
    try:
        summary_stats = cleaned_df.describe(include='all').to_string()
        with open(stats_file, "w") as f:
            f.write("Summary Statistics for Cleaned Data\n")
            f.write("=" * 50 + "\n\n")
            f.write(summary_stats)
            f.write("\n\n***** Processing Log *****\n")
            f.write("\n".join(log))
        print(f"Summary statistics and log saved as {stats_file}")
    except Exception as e:
        print(f"Error saving summary statistics: {e}")

if __name__ == "__main__":
    main()
