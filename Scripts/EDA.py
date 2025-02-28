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
    Compute key statistical metrics for numerical features and save to "Statistical_Summary.txt".
    Also compute skewness and kurtosis for each numeric column.
    """
    summary = df.describe(include='all')
    num_cols = df.select_dtypes(include=[np.number]).columns
    
    extra_stats = pd.DataFrame({
        'skewness': df[num_cols].skew(),
        'kurtosis': df[num_cols].kurtosis()
    })
    
    # Insert skewness & kurtosis into the summary
    for col in num_cols:
        summary.loc[col, 'skewness'] = extra_stats.loc[col, 'skewness']
        summary.loc[col, 'kurtosis'] = extra_stats.loc[col, 'kurtosis']
    
    output_file = os.path.join(output_dir, "Statistical_Summary.txt")
    with open(output_file, "w") as f:
        f.write("Statistical Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(summary.to_string())
    print(f"Statistical summary saved as {output_file}")

# ======================= 2) Time Series Analysis =======================
def time_series_analysis(df, output_dir):
    """
    Plot 'value' over time. We assume 'date' or 'period' is the datetime column.
    The plot is saved as "Time_Series_Analysis.png".
    """
    # Pick whichever datetime column you have
    if 'date' in df.columns:
        time_col = 'date'
    elif 'period' in df.columns:
        time_col = 'period'
    else:
        raise ValueError("No column named 'date' or 'period' found for time series analysis.")
    
    # Convert to datetime
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df_sorted = df.sort_values(by=time_col).dropna(subset=[time_col, 'value'])
    
    plt.figure(figsize=(12,6))
    plt.plot(df_sorted[time_col], df_sorted['value'], label='Electricity Demand', color='blue')
    plt.xlabel("Time")
    plt.ylabel("Electricity Demand")
    plt.title("Electricity Demand Over Time")
    plt.legend()
    plt.grid(True)
    
    # Optionally annotate max & min
    max_idx = df_sorted['value'].idxmax()
    min_idx = df_sorted['value'].idxmin()
    plt.annotate("Max Demand",
                 xy=(df_sorted.loc[max_idx, time_col], df_sorted.loc[max_idx, 'value']),
                 xytext=(10, 10),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->", color='green'))
    plt.annotate("Min Demand",
                 xy=(df_sorted.loc[min_idx, time_col], df_sorted.loc[min_idx, 'value']),
                 xytext=(10, -20),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->", color='red'))
    
    output_file = os.path.join(output_dir, "Time_Series_Analysis.png")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Time series analysis plot saved as {output_file}")

# ======================= 3) Univariate Analysis =======================
def univariate_analysis(df, output_dir):
    """
    Generate histograms, boxplots, and density plots for numeric columns,
    saved as "Univariate_Analysis.png".
    """
    # Select numeric columns, excluding any that might not be relevant
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Create subplots: 3 subplots (hist, box, density) for each numeric column
    n = len(num_cols)
    fig, axes = plt.subplots(n, 3, figsize=(18, 4*n))
    
    # If only one numeric column, axes is not a 2D array
    if n == 1:
        axes = np.array([axes])
    
    for i, col in enumerate(num_cols):
        col_data = df[col].dropna()
        
        # Histogram
        axes[i, 0].hist(col_data, bins=30, color='skyblue', edgecolor='black')
        axes[i, 0].set_title(f"Histogram of {col}")
        axes[i, 0].set_xlabel(col)
        axes[i, 0].set_ylabel("Frequency")
        
        # Boxplot
        axes[i, 1].boxplot(col_data, vert=False)
        axes[i, 1].set_title(f"Boxplot of {col}")
        axes[i, 1].set_xlabel(col)
        
        # Density
        col_data.plot(kind='density', ax=axes[i, 2], color='purple')
        axes[i, 2].set_title(f"Density of {col}")
        axes[i, 2].set_xlabel(col)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, "Univariate_Analysis.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Univariate analysis plots saved as {output_file}")

# ======================= 4) Correlation Analysis =======================
def correlation_analysis(df, output_dir):
    """
    Compute correlation matrix for relevant numeric columns, plot a heatmap,
    and save as "Correlation_Analysis.png".
    """
    # If you specifically want to analyze certain columns, define them here:
    # They must exist in df.columns, or else skip them
    desired_cols = [
        'value', 'temperature_2m', 'extracted_period_hour', 'extracted_period_day',
        'extracted_period_month', 'extracted_period_dayofweek',
        'extracted_date_hour', 'extracted_date_day', 'extracted_date_month',
        'extracted_date_dayofweek', 'value_std', 'temperature_2m_std'
    ]
    existing_cols = [c for c in desired_cols if c in df.columns]
    
    # If none exist, fallback to numeric columns
    if not existing_cols:
        existing_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Compute correlation on the existing columns
    corr = df[existing_cols].corr()
    
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Matrix")
    
    output_file = os.path.join(output_dir, "Correlation_Analysis.png")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Correlation analysis heatmap saved as {output_file}")

# ======================= 5) Advanced Time Series Techniques =======================
def advanced_time_series_techniques(df, output_dir):
    """
    Time series decomposition + ADF test. Saved as:
      - "Advanced_Time_Series_Techniques.png" for decomposition plot
      - "Advanced_Time_Series_Techniques.txt" for ADF test results
    """
    # Use 'date' if it exists, otherwise 'period'
    if 'date' in df.columns:
        time_col = 'date'
    elif 'period' in df.columns:
        time_col = 'period'
    else:
        raise ValueError("No date or period column found for time series decomposition.")
    
    # Convert to datetime & sort
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df_sorted = df.sort_values(by=time_col).dropna(subset=[time_col, 'value'])
    
    # Create a time series (index = date, values = 'value')
    ts = df_sorted.set_index(time_col)['value']
    
    # Decompose (assume hourly data with period=24, adjust if needed)
    decomposition = seasonal_decompose(ts, model='additive', period=24)
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    out_plot = os.path.join(output_dir, "Advanced_Time_Series_Techniques.png")
    plt.tight_layout()
    plt.savefig(out_plot)
    plt.close()
    print(f"Time series decomposition plot saved as {out_plot}")
    
    # Augmented Dickey-Fuller test
    adf_result = adfuller(ts.dropna())
    adf_text = (
        f"ADF Statistic: {adf_result[0]:.4f}\n"
        f"p-value: {adf_result[1]:.4f}\n"
        f"# Lags Used: {adf_result[2]}\n"
        f"Number of Observations Used: {adf_result[3]}\n"
        "Critical Values:\n"
    )
    for key, val in adf_result[4].items():
        adf_text += f"    {key}: {val:.4f}\n"
    
    out_txt = os.path.join(output_dir, "Advanced_Time_Series_Techniques.txt")
    with open(out_txt, "w") as f:
        f.write("Augmented Dickey-Fuller Test Results\n")
        f.write("=" * 40 + "\n")
        f.write(adf_text)
    print(f"ADF test results saved as {out_txt}")

# ======================= Main EDA Function =======================
def run_eda(input_csv, output_dir):
    """
    Load the cleaned dataset from input_csv, run all EDA functions,
    and save the outputs in output_dir.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df = pd.read_csv(input_csv)
    print(f"Loaded dataset with shape: {df.shape}")
    
    # 1) Statistical Summary
    statistical_summary(df, output_dir)
    
    # 2) Time Series Analysis
    time_series_analysis(df, output_dir)
    
    # 3) Univariate Analysis
    univariate_analysis(df, output_dir)
    
    # 4) Correlation Analysis
    correlation_analysis(df, output_dir)
    
    # 5) Advanced Time Series Techniques
    advanced_time_series_techniques(df, output_dir)
    
    print("All EDA analyses completed and saved.")

# ======================= Script Entry Point =======================
if __name__ == "__main__":
    # Example usage
    source_csv = r"E:\programing\Data Science\Assignment 2\Outputs\Cleaned Dateset\cleaned_output.csv"
    eda_output_dir = r"E:\programing\Data Science\Assignment 2\Outputs\EDA"
    
    run_eda(source_csv, eda_output_dir)

