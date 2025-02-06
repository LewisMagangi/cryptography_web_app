import pandas as pd
import os

def calculate_rate(row):
    """Calculate rate from file size and time taken"""
    if pd.isna(row['rate']) or row['rate'] == '':
        try:
            # Extract file size from filename (e.g., '50bytes_text_data_faker.txt' -> 50)
            file_size = int(row['file_name'].split('bytes')[0])
            time_taken = float(row['time_taken'])
            
            # Calculate rate (bytes per second)
            if time_taken > 0:
                return file_size / time_taken
            return 0
        except:
            return 0
    return row['rate']

def update_rates():
    # Get the path to results file
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(project_root, 'analysis', 'data', 'results', 'asymmetric_analysis_results.csv')
    
    # Read the CSV
    df = pd.read_csv(csv_path)
    
    # Update rates
    df['rate'] = df.apply(calculate_rate, axis=1)
    
    # Save updated CSV
    df.to_csv(csv_path, index=False)
    print(f"Updated rates in {csv_path}")

if __name__ == "__main__":
    update_rates()
