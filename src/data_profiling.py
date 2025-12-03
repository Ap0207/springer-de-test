import os
import glob
import pandas as pd

# Define paths
DATA_DIR = '/home/apurvraj/springer_de_project/data/'
OUTPUT_DIR = '/home/apurvraj/springer_de_project/docs/'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'data_dictionary.xlsx')

def profile_data():
    # 1. Get all CSV files in the data directory
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    
    if not csv_files:
        print("No CSV files found in 'data/' directory!")
        return

    all_profiles = []

    print(f"Found {len(csv_files)} files. Starting profiling...")

    # 2. Loop through each file
    for file_path in csv_files:
        table_name = os.path.basename(file_path)
        print(f"Processing: {table_name}")
        
        try:
            # Load data
            df = pd.read_csv(file_path)
            total_rows = len(df)

            # 3. Analyze each column
            for col in df.columns:
                col_data = df[col]
                
                # Calculate metrics
                dtype = str(col_data.dtype)
                null_count = col_data.isnull().sum()
                # Percentage of non-null values
                pct_populated = 100 * (1 - (null_count / total_rows)) if total_rows > 0 else 0
                distinct_count = col_data.nunique()
                
                # handle min/max safely (convert to string to avoid comparison errors)
                try:
                    min_val = col_data.min()
                    max_val = col_data.max()
                except:
                    min_val = "N/A"
                    max_val = "N/A"

                # Append to list
                all_profiles.append({
                    "Table Name": table_name,
                    "Column Name": col,
                    "Data Type": dtype,
                    "Total Rows": total_rows,
                    "Null Count": null_count,
                    "Pct Populated": round(pct_populated, 2),
                    "Distinct Values": distinct_count,
                    "Min Value": str(min_val)[:50], # Truncate long strings
                    "Max Value": str(max_val)[:50]
                })
        except Exception as e:
            print(f"Error processing {table_name}: {e}")

    # 4. Save to Excel
    if all_profiles:
        profile_df = pd.DataFrame(all_profiles)
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        profile_df.to_excel(OUTPUT_FILE, index=False)
        print(f"\n✅ Success! Data dictionary saved to: {OUTPUT_FILE}")
    else:
        print("No data could be profiled.")

if __name__ == "__main__":
    profile_data()
