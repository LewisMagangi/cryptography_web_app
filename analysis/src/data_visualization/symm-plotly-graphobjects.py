import os
import pandas as pd
import plotly.graph_objects as go

# Define the path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'results', 'symmetric_analysis_results.csv')

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
algorithms = ['AES', 'DES', '3DES', 'RC2', 'RC4', 'Blowfish']
file_names = ['10mb_text_data_faker.txt', '20mb_text_data_faker.txt', '30mb_text_data_faker.txt', '40mb_text_data_faker.txt', '50mb_text_data_faker.txt']

# Iterate through algorithms and file names
for algorithm in algorithms:
    for file_name in file_names:
        data = create_data_dict(algorithm, file_name)
        df = pd.DataFrame(data)

        # Create the chart using plotly.graph_objects
        fig = go.Figure()

        # Add bars for each key_size and operation
        fig.add_trace(go.Bar(
            name='Encryption',
            x=df[df['operation'] == 'encryption']['key_size'],
            y=df[df['operation'] == 'encryption']['time_taken'],
            marker_color='blue'
        ))

        fig.add_trace(go.Bar(
            name='Decryption',
            x=df[df['operation'] == 'decryption']['key_size'],
            y=df[df['operation'] == 'decryption']['time_taken'],
            marker_color='green'
        ))

        # Change the bar mode
        fig.update_layout(
            barmode='group',
            title=f'{algorithm} Encryption/Decryption Time vs. Key Size ({file_name})',
            xaxis_title='Key Size',
            yaxis_title='Time Taken (seconds)'
        )

        # Define the path to save the plot
        PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'symmetric_analysis', 'barchart', 'grouped')
        os.makedirs(PLOT_DIR, exist_ok=True)
        PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_graphobject.png')

        # Save the plot
        fig.write_image(PLOT_PATH)

        # Show the plot
        fig.show()