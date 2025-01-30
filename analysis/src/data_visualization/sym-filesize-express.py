import os
import pandas as pd
import plotly.express as px

# Define the path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'results', 'symmetric_analysis_results.csv')

def create_data_dict(algorithm, key_size):
    # Load data from the CSV file
    df = pd.read_csv(CSV_PATH)
    
    # Filter the DataFrame based on the provided algorithm and key size
    filtered_df = df[(df['algorithm'] == algorithm) & (df['key_size'] == key_size)].copy()
    
    # Clean the file names
    filtered_df['file_size'] = filtered_df['file_name'].str.extract(r'(\d+mb|\d+kb|\d+bytes)')
    
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

        # Create the grouped bar chart
        fig = px.bar(df, 
                     x='file_size', 
                     y='time_taken', 
                     color='operation', 
                     barmode='group',
                     title=f'{algorithm} Encryption and Decryption Time vs. File Size (Key Size: {key_size})')

        # Set labels
        fig.update_layout(
            xaxis_title='File Size',
            yaxis_title='Time Taken (seconds)'
        )

        # Define the path to save the plot
        PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'symmetric_analysis', 'barchart', 'filesize')
        os.makedirs(PLOT_DIR, exist_ok=True)
        PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_keysize_{key_size}_filesize_express.png')

        # Save the plot
        fig.write_image(PLOT_PATH)

        # Show the plot
        fig.show()