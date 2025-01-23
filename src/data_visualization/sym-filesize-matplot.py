import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'results', 'symmetric_analysis_results.csv')

def create_data_dict(algorithm, key_size):
    # Load data from the CSV file
    df = pd.read_csv(CSV_PATH)
    
    # Filter the DataFrame and create an explicit copy to avoid warnings
    filtered_df = df[(df['algorithm'] == algorithm) & (df['key_size'] == key_size)].copy()
    
    # Extract file sizes safely
    filtered_df.loc[:, 'file_size'] = filtered_df['file_name'].str.extract(r'(\d+mb|\d+kb|\d+bytes)')
    
    # Create the data dictionary
    data = {
        'algorithm': [algorithm] * len(filtered_df),
        'operation': filtered_df['operation'].tolist(),
        'file_size': filtered_df['file_size'].dropna().tolist(),  # Remove NaN values
        'key_size': [key_size] * len(filtered_df),
        'time_taken': filtered_df['time_taken'].tolist()
    }
    return data

# List of algorithms and their respective key sizes
algorithms_key_sizes = {
    'AES': [16, 24, 32],
    'DES': [8],
    '3DES': [16, 24],
    'RC2': [5, 8, 16],
    'RC4': [5, 8, 16],
    'Blowfish': [4, 8, 16, 24, 32]
}

# Iterate through algorithms and key sizes
for algorithm, key_sizes in algorithms_key_sizes.items():
    for key_size in key_sizes:
        data = create_data_dict(algorithm, key_size)
        df = pd.DataFrame(data)
        
        if df.empty:
            continue  # Skip if there is no data
        
        # Create the grouped bar chart
        plt.figure(figsize=(10, 6))
        
        # Handle file sizes on the x-axis safely
        unique_file_sizes = df['file_size'].dropna().unique()
        x = range(len(unique_file_sizes))
        bar_width = 0.35
        
        if not df[df['operation'] == 'encryption'].empty:
            plt.bar(x, df[df['operation'] == 'encryption']['time_taken'], 
                    width=bar_width, label='Encryption', color='blue')
        if not df[df['operation'] == 'decryption'].empty:
            plt.bar([p + bar_width for p in x], df[df['operation'] == 'decryption']['time_taken'], 
                    width=bar_width, label='Decryption', color='green')
        
        # Set labels and title
        plt.xlabel('File Size')
        plt.ylabel('Time Taken (seconds)')
        plt.title(f'{algorithm} Encryption and Decryption Time vs. File Size (Key Size: {key_size})')
        plt.xticks([p + bar_width / 2 for p in x], unique_file_sizes, rotation=45)
        plt.legend()
        
        # Define the path to save the plot
        PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'symmetric_analysis', 'barchart', 'filesize')
        os.makedirs(PLOT_DIR, exist_ok=True)
        PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_keysize_{key_size}_filesize_matplotlib.png')
        
        # Save the plot
        plt.savefig(PLOT_PATH)
        
        # Show the plot
        plt.show()
