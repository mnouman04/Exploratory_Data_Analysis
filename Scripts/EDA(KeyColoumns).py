
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# ======================= 1) Statistical Summary =======================
def statistical_summary(df, output_dir):
    """
    Compute key statistical metrics for selected numerical features and save to "Statistical_Summary.txt".
    """
    key_features = ['value', 'temperature_2m', 'extracted_period_hour',
                    'extracted_period_day', 'extracted_period_month', 'extracted_period_dayofweek']
    existing_features = [col for col in key_features if col in df.columns]
    
    summary = df[existing_features].describe()
    extra_stats = pd.DataFrame({
        'skewness': df[existing_features].skew(),
        'kurtosis': df[existing_features].kurtosis()
    })
    summary = pd.concat([summary, extra_stats])

    
    output_file = os.path.join(output_dir, "Statistical_Summary.txt")
    summary.to_csv(output_file, sep='\t')
    print(f"Statistical summary saved as {output_file}")

# ======================= 2) Time Series Analysis =======================
def time_series_analysis(df, output_dir):
    """
    Plot electricity demand over time.
    """
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_sorted = df.sort_values(by='date').dropna(subset=['date', 'value'])
    
    plt.figure(figsize=(12,6))
    plt.plot(df_sorted['date'], df_sorted['value'], label='Electricity Demand', color='blue')
    plt.xlabel("Time")
    plt.ylabel("Electricity Demand")
    plt.title("Electricity Demand Over Time")
    plt.legend()
    plt.grid(True)
    
    output_file = os.path.join(output_dir, "Time_Series_Analysis.png")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Time series analysis plot saved as {output_file}")

# ======================= 3) Univariate Analysis =======================
def univariate_analysis(df, output_dir):
    """
    Generate histograms, boxplots, and density plots for key numerical features.
    """
    key_features = ['value', 'temperature_2m']
    df = df[key_features].dropna()
    
    fig, axes = plt.subplots(len(key_features), 3, figsize=(15, 5*len(key_features)))
    
    for i, col in enumerate(key_features):
        col_data = df[col]
        
        sns.histplot(col_data, bins=30, kde=True, ax=axes[i, 0], color='skyblue')
        axes[i, 0].set_title(f"Histogram of {col}")
        
        sns.boxplot(x=col_data, ax=axes[i, 1], color='lightcoral')
        axes[i, 1].set_title(f"Boxplot of {col}")
        
        sns.kdeplot(col_data, ax=axes[i, 2], color='purple')
        axes[i, 2].set_title(f"Density Plot of {col}")
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, "Univariate_Analysis.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Univariate analysis plots saved as {output_file}")

# ======================= 4) Correlation Analysis =======================
def correlation_analysis(df, output_dir):
    """
    Compute correlation matrix and visualize using a heatmap.
    """
    key_features = ['value', 'temperature_2m', 'extracted_period_hour',
                    'extracted_period_day', 'extracted_period_month', 'extracted_period_dayofweek']
    df = df[key_features].dropna()
    
    plt.figure(figsize=(8,6))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Matrix")
    
    output_file = os.path.join(output_dir, "Correlation_Analysis.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Correlation analysis heatmap saved as {output_file}")

# ======================= 5) Advanced Time Series Techniques =======================
def advanced_time_series_techniques(df, output_dir):
    """
    Perform time series decomposition and ADF test.
    """
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_sorted = df.sort_values(by='date').dropna(subset=['date', 'value'])
    ts = df_sorted.set_index('date')['value']
    
    decomposition = seasonal_decompose(ts, model='additive', period=24)
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, "Advanced_Time_Series_Techniques.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Time series decomposition plot saved as {output_file}")
    
    adf_result = adfuller(ts.dropna())
    adf_output = (f"ADF Statistic: {adf_result[0]:.4f}\n"
                  f"p-value: {adf_result[1]:.4f}\n"
                  f"Critical Values: {adf_result[4]}")
    
    output_file_txt = os.path.join(output_dir, "ADF_Test_Results.txt")
    with open(output_file_txt, "w") as f:
        f.write(adf_output)
    print(f"ADF test results saved as {output_file_txt}")

# ======================= Main EDA Function =======================
def run_eda(input_csv, output_dir):
    """
    Load dataset, run all EDA functions, and save outputs.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df = pd.read_csv(input_csv)
    print(f"Loaded dataset with shape: {df.shape}")
    
    statistical_summary(df, output_dir)
    time_series_analysis(df, output_dir)
    univariate_analysis(df, output_dir)
    correlation_analysis(df, output_dir)
    advanced_time_series_techniques(df, output_dir)
    
    print("All EDA analyses completed and saved.")

# ======================= Script Entry Point =======================
if __name__ == "__main__":
    source_csv = "E:\programing\Data Science\Assignment 2\Outputs\Cleaned Dateset\cleaned_output.csv"
    eda_output_dir = "E:\programing\Data Science\Assignment 2\Outputs\EDA\KeyNumericals"
    run_eda(source_csv, eda_output_dir)
