import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
import os

# ------------------------------------------------------------------------------
# 1. Set up paths and filenames
# ------------------------------------------------------------------------------
input_file = "E:\programing\Data Science\Assignment 2\Outputs\Cleaned Dateset\cleaned_output.csv"           # Original CSV
output_file = "E:\programing\Data Science\Assignment 2\Outputs\OuttliersDetection\cleaned_data.csv"       # Cleaned CSV
report_file = "E:\programing\Data Science\Assignment 2\Outputs\OuttliersDetection\outlier_handling.txt"   # Text report
plot_dir = "E:\programing\Data Science\Assignment 2\Outputs\OuttliersDetection\plots" 
# ------------------------------------------------------------------------------
## ------------------------------------------------------------------------------
# 2. Read the dataset
# ------------------------------------------------------------------------------
df = pd.read_csv(input_file)

# Numerical columns for outlier detection
num_cols = ["value", "temperature_2m", "value_std", "temperature_2m_std"]

# Create a directory for plots if it doesn't exist
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# ------------------------------------------------------------------------------
# 3. Define helper functions
# ------------------------------------------------------------------------------
def detect_outliers_iqr(data, column):
    """
    Returns a boolean Series where True indicates an outlier
    based on the 1.5 * IQR rule, along with the IQR boundaries.
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (data[column] < lower_bound) | (data[column] > upper_bound), lower_bound, upper_bound

def detect_outliers_zscore(data, column, threshold=3):
    """
    Returns a boolean Series where True indicates an outlier
    based on the Z-score threshold.
    """
    return np.abs(zscore(data[column])) > threshold

def plot_before_after(df_original, df_capped, column):
    """
    Creates side-by-side boxplots for before and after outlier handling.
    Saves the figure as a PNG file.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    # Before
    axes[0].boxplot(df_original[column].dropna(), vert=True)
    axes[0].set_title(f"Before Capping - {column}")
    
    # After
    axes[1].boxplot(df_capped[column].dropna(), vert=True)
    axes[1].set_title(f"After Capping - {column}")
    
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f"{column}_before_after.png"))
    plt.close()

# ------------------------------------------------------------------------------
# 4. Copy original data for plotting comparisons
# ------------------------------------------------------------------------------
df_original = df.copy()

# ------------------------------------------------------------------------------
# 5. Detect & handle outliers (Winsorization)
# ------------------------------------------------------------------------------
outlier_summary = []
total_outliers = 0

for col in num_cols:
    if col in df.columns:
        # IQR-based detection
        iqr_mask, lower_bound, upper_bound = detect_outliers_iqr(df, col)
        
        # Z-score detection
        z_mask = detect_outliers_zscore(df, col)
        
        # Combine both outlier masks (logical OR)
        combined_mask = iqr_mask | z_mask
        
        # Count outliers before capping
        outlier_count = combined_mask.sum()
        total_outliers += outlier_count
        
        # Record summary
        outlier_summary.append({
            "column": col,
            "iqr_outliers": iqr_mask.sum(),
            "zscore_outliers": z_mask.sum(),
            "combined_outliers": outlier_count,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        })
        
        # Winsorize/cap outliers
        df.loc[df[col] < lower_bound, col] = lower_bound
        df.loc[df[col] > upper_bound, col] = upper_bound

# ------------------------------------------------------------------------------
# 6. Plot before-and-after for each numeric column
# ------------------------------------------------------------------------------
for col in num_cols:
    if col in df.columns:
        plot_before_after(df_original, df, col)

# ------------------------------------------------------------------------------
# 7. Generate a text report
# ------------------------------------------------------------------------------
with open(report_file, "w") as f:
    f.write("Outlier Handling Report\n")
    f.write("======================\n\n")
    
    f.write("Column-by-Column Summary:\n")
    for summary in outlier_summary:
        f.write(
            f"- {summary['column']}:\n"
            f"   IQR outliers: {summary['iqr_outliers']}\n"
            f"   Z-score outliers: {summary['zscore_outliers']}\n"
            f"   Combined outliers: {summary['combined_outliers']}\n"
            f"   Capping range: [{summary['lower_bound']:.2f}, {summary['upper_bound']:.2f}]\n\n"
        )
    
    f.write(f"Total Outliers (across all columns): {total_outliers}\n\n")
    
    f.write("Technical Rationale:\n")
    f.write("- Outliers can distort mean/variance, affect model performance, and skew visualizations.\n")
    f.write("- By capping rather than removing, we retain data size while mitigating extreme skew.\n\n")
    
    f.write("Before-and-After Visualizations:\n")
    f.write("  Boxplots have been saved in the 'plots' directory for each numeric column.\n\n")
    
    f.write("Decision:\n")
    f.write("  We applied capping (winsorization) based on IQR boundaries.\n")

# ------------------------------------------------------------------------------
# 8. Save the cleaned dataset (no extra columns added)
# ------------------------------------------------------------------------------
df.to_csv(output_file, index=False)

print("Outlier detection, capping, and reporting complete.")
print(f"Cleaned data saved to: {output_file}")
print(f"Report saved to: {report_file}")
print(f"Plots saved to directory: {plot_dir}")