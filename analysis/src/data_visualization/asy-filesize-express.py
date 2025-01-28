import os
import pandas as pd
import plotly.express as px

# Define the path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'results', 'asymmetric_analysis_results.csv')

def parse_file_size(file_name):
    return int(file_name.split('bytes')[0])  # Extract the bytes size from the file name

def create_data_dict(algorithm, key_size):
    # Load data from the CSV file
    df = pd.read_csv(CSV_PATH)

    # Filter the DataFrame based on the provided algorithm and key size
    filtered_df = df[(df['algorithm'] == algorithm) & (df['key_size'] == key_size)]

    # Create the data dictionary
    data = {
        'algorithm': [algorithm] * len(filtered_df),
        'operation': filtered_df['operation'].tolist(),
        'file_size': [parse_file_size(fname) for fname in filtered_df['file_name'].tolist()],
        'key_size': [key_size] * len(filtered_df),
        'time_taken': filtered_df['time_taken'].tolist()
    }
    return data

# List of algorithms and key sizes
algorithms = ['RSA', 'DSA', 'DH', 'ECC']
key_sizes = ['1024', '2048', '3072', '4096', 'P-256', 'P-384', 'P-521']

# Iterate through algorithms and key sizes
for algorithm in algorithms:
    for key_size in key_sizes:
        data = create_data_dict(algorithm, key_size)
        df = pd.DataFrame(data)

        # Skip if the DataFrame is empty
        if df.empty:
            continue

        # Sort the DataFrame by file_size
        df = df.sort_values(by='file_size')

        # Create the grouped bar chart for signing and verification
        if algorithm in ['RSA', 'DSA', 'ECC']:
            fig = px.bar(df[df['operation'].isin(['signing', 'verification'])], 
                         x='file_size', 
                         y='time_taken', 
                         color='operation', 
                         barmode='group',
                         title=f'{algorithm} Signing and Verification Time vs. File Size (Key Size: {key_size})')

            # Set labels
            fig.update_layout(
                xaxis_title='File Size (bytes)',
                yaxis_title='Time Taken (seconds)'
            )

            # Define the path to save the plot
            PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'asymmetric_analysis', 'barchart', 'grouped')
            os.makedirs(PLOT_DIR, exist_ok=True)
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{key_size}_signing_verification_express.png')

            # Save the plot
            fig.write_image(PLOT_PATH)

            # Show the plot
            fig.show()

        # Create the grouped bar chart for encryption and decryption (if applicable)
        if algorithm in ['RSA']:
            fig = px.bar(df[df['operation'].isin(['encryption', 'decryption'])], 
                         x='file_size', 
                         y='time_taken', 
                         color='operation', 
                         barmode='group',
                         title=f'{algorithm} Encryption and Decryption Time vs. File Size (Key Size: {key_size})')

            # Set labels
            fig.update_layout(
                xaxis_title='File Size (bytes)',
                yaxis_title='Time Taken (seconds)'
            )

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{key_size}_encryption_decryption_express.png')

            # Save the plot
            fig.write_image(PLOT_PATH)

            # Show the plot
            fig.show()

        # Create the grouped bar chart for key exchange (if applicable)
        if algorithm == 'DH':
            fig = px.bar(df[df['operation'] == 'key_exchange'], 
                         x='file_size', 
                         y='time_taken', 
                         color='operation', 
                         barmode='group',
                         title=f'{algorithm} Key Exchange Time vs. File Size (Key Size: {key_size})')

            # Set labels
            fig.update_layout(
                xaxis_title='File Size (bytes)',
                yaxis_title='Time Taken (seconds)'
            )

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{key_size}_key_exchange_express.png')

            # Save the plot
            fig.write_image(PLOT_PATH)

            # Show the plot
            fig.show()