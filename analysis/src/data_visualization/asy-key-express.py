import os
import pandas as pd
import plotly.express as px

# Define the path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'results', 'asymmetric_analysis_results.csv')

def create_data_dict(algorithm, file_name):
    # Load data from the CSV file
    df = pd.read_csv(CSV_PATH)
    
    # Filter the DataFrame based on the provided algorithm and file name
    filtered_df = df[(df['algorithm'] == algorithm) & (df['file_name'] == file_name)]
    
    # Create the data dictionary
    data = {
        'algorithm': [algorithm] * len(filtered_df),
        'operation': filtered_df['operation'].tolist(),
        'key_size': filtered_df['key_size'].tolist(),
        'file_name': [file_name] * len(filtered_df),
        'time_taken': filtered_df['time_taken'].tolist()
    }
    return data

# List of algorithms and file names
algorithms = ['RSA', 'DSA', 'DH', 'ECC']
file_names = ['50bytes_text_data_faker.txt', '100bytes_text_data_faker.txt', '150bytes_text_data_faker.txt', '200bytes_text_data_faker.txt']

# Iterate through algorithms and file names
for algorithm in algorithms:
    for file_name in file_names:
        data = create_data_dict(algorithm, file_name)
        df = pd.DataFrame(data)

        # Create the grouped bar chart for signing and verification
        if algorithm in ['RSA', 'DSA', 'ECC']:
            fig = px.bar(df[df['operation'].isin(['signing', 'verification'])], 
                         x='key_size', 
                         y='time_taken', 
                         color='operation', 
                         barmode='group',
                         title=f'{algorithm} Signing and Verification Time vs. Key Size ({file_name})')

            # Set labels
            fig.update_layout(
                xaxis_title='Key Size',
                yaxis_title='Time Taken (seconds)'
            )

            # Define the path to save the plot
            PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'asymmetric_analysis', 'barchart', 'grouped')
            os.makedirs(PLOT_DIR, exist_ok=True)
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_signing_verification_express.png')

            # Save the plot
            fig.write_image(PLOT_PATH)

            # Show the plot
            fig.show()

        # Create the grouped bar chart for encryption and decryption (if applicable)
        if algorithm in ['RSA']:
            fig = px.bar(df[df['operation'].isin(['encryption', 'decryption'])], 
                         x='key_size', 
                         y='time_taken', 
                         color='operation', 
                         barmode='group',
                         title=f'{algorithm} Encryption and Decryption Time vs. Key Size ({file_name})')

            # Set labels
            fig.update_layout(
                xaxis_title='Key Size',
                yaxis_title='Time Taken (seconds)'
            )

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_encryption_decryption_express.png')

            # Save the plot
            fig.write_image(PLOT_PATH)

            # Show the plot
            fig.show()

        # Create the grouped bar chart for key exchange (if applicable)
        if algorithm == 'DH':
            fig = px.bar(df[df['operation'] == 'key_exchange'], 
                         x='key_size', 
                         y='time_taken', 
                         color='operation', 
                         barmode='group',
                         title=f'{algorithm} Key Exchange Time vs. Key Size ({file_name})')

            # Set labels
            fig.update_layout(
                xaxis_title='Key Size',
                yaxis_title='Time Taken (seconds)'
            )

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_key_exchange_express.png')

            # Save the plot
            fig.write_image(PLOT_PATH)

            # Show the plot
            fig.show()