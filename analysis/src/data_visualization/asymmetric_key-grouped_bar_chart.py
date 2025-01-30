import os
import pandas as pd
import matplotlib.pyplot as plt

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
            plt.figure(figsize=(10, 6))

            # Handle numeric and string key sizes separately
            if df['key_size'].dtype == 'object':
                # For string key sizes (e.g., ECC)
                bar_width = 0.15
                x = range(len(df['key_size'].unique()))
                if not df[df['operation'] == 'signing'].empty:
                    plt.bar(x, df[df['operation'] == 'signing']['time_taken'], 
                            width=bar_width, label='Signing', color='red')
                if not df[df['operation'] == 'verification'].empty:
                    plt.bar([p + bar_width for p in x], df[df['operation'] == 'verification']['time_taken'], 
                            width=bar_width, label='Verification', color='orange')
                plt.xticks([p + bar_width for p in x], df['key_size'].unique())
            else:
                # For numeric key sizes
                bar_width = 0.15
                x = range(len(df['key_size'].unique()))
                if not df[df['operation'] == 'signing'].empty:
                    plt.bar(x, df[df['operation'] == 'signing']['time_taken'], 
                            width=bar_width, label='Signing', color='red')
                if not df[df['operation'] == 'verification'].empty:
                    plt.bar([p + bar_width for p in x], df[df['operation'] == 'verification']['time_taken'], 
                            width=bar_width, label='Verification', color='orange')
                plt.xticks([p + bar_width for p in x], df['key_size'].unique())

            # Set labels and title
            plt.xlabel('Key Size')
            plt.ylabel('Time Taken (seconds)')
            plt.title(f'{algorithm} Signing and Verification Time vs. Key Size ({file_name})')
            plt.xticks(rotation=45)
            plt.legend()

            # Define the path to save the plot
            PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'asymmetric_analysis', 'barchart', 'grouped')
            os.makedirs(PLOT_DIR, exist_ok=True)
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_signing_verification_matplotlib.png')

            # Save the plot
            plt.savefig(PLOT_PATH)

            # Show the plot
            plt.show()

        # Create the grouped bar chart for encryption and decryption (if applicable)
        if algorithm in ['RSA']:
            plt.figure(figsize=(10, 6))
            if not df[df['operation'] == 'encryption'].empty:
                plt.bar(x, df[df['operation'] == 'encryption']['time_taken'], 
                        width=bar_width, label='Encryption', color='blue')
            if not df[df['operation'] == 'decryption'].empty:
                plt.bar([p + bar_width for p in x], df[df['operation'] == 'decryption']['time_taken'], 
                        width=bar_width, label='Decryption', color='green')
            plt.xticks([p + bar_width for p in x], df['key_size'].unique())

            # Set labels and title
            plt.xlabel('Key Size')
            plt.ylabel('Time Taken (seconds)')
            plt.title(f'{algorithm} Encryption and Decryption Time vs. Key Size ({file_name})')
            plt.xticks(rotation=45)
            plt.legend()

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_encryption_decryption_matplotlib.png')

            # Save the plot
            plt.savefig(PLOT_PATH)

            # Show the plot
            plt.show()

        # Create the grouped bar chart for key exchange (if applicable)
        if algorithm == 'DH':
            plt.figure(figsize=(10, 6))
            if not df[df['operation'] == 'key_exchange'].empty:
                plt.bar(x, df[df['operation'] == 'key_exchange']['time_taken'], 
                        width=bar_width, label='Key Exchange', color='purple')
            plt.xticks([p + bar_width for p in x], df['key_size'].unique())

            # Set labels and title
            plt.xlabel('Key Size')
            plt.ylabel('Time Taken (seconds)')
            plt.title(f'{algorithm} Key Exchange Time vs. Key Size ({file_name})')
            plt.xticks(rotation=45)
            plt.legend()

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{file_name}_key_exchange_matplotlib.png')

            # Save the plot
            plt.savefig(PLOT_PATH)

            # Show the plot
            plt.show()
import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'results', 'asymmetric_analysis_results.csv')

def create_data_dict(algorithm, key_size):
    # Load data from the CSV file
    df = pd.read_csv(CSV_PATH)

    # Filter the DataFrame based on the provided algorithm and key size
    filtered_df = df[(df['algorithm'] == algorithm) & (df['key_size'] == key_size)]

    # Create the data dictionary
    data = {
        'algorithm': [algorithm] * len(filtered_df),
        'operation': filtered_df['operation'].tolist(),
        'file_size': filtered_df['file_name'].tolist(),  # Replace key_size with file_name
        'key_size': [key_size] * len(filtered_df),
        'time_taken': filtered_df['time_taken'].tolist()
    }
    return data

# List of algorithms and key sizes
algorithms = ['RSA', 'DSA', 'DH', 'ECC']
key_sizes = ['1024', '2048', '3072', '4096']

# Iterate through algorithms and key sizes
for algorithm in algorithms:
    for key_size in key_sizes:
        data = create_data_dict(algorithm, key_size)
        df = pd.DataFrame(data)

        # Create the grouped bar chart for signing and verification
        if algorithm in ['RSA', 'DSA', 'ECC']:
            plt.figure(figsize=(10, 6))

            bar_width = 0.15
            x = range(len(df['file_size'].unique()))
            if not df[df['operation'] == 'signing'].empty:
                plt.bar(x, df[df['operation'] == 'signing']['time_taken'],
                        width=bar_width, label='Signing', color='red')
            if not df[df['operation'] == 'verification'].empty:
                plt.bar([p + bar_width for p in x], df[df['operation'] == 'verification']['time_taken'],
                        width=bar_width, label='Verification', color='orange')
            plt.xticks([p + bar_width for p in x], df['file_size'].unique())

            # Set labels and title
            plt.xlabel('File Size')
            plt.ylabel('Time Taken (seconds)')
            plt.title(f'{algorithm} Signing and Verification Time vs. File Size (Key Size: {key_size})')
            plt.xticks(rotation=45)
            plt.legend()

            # Define the path to save the plot
            PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'media', 'plots', 'asymmetric_analysis', 'barchart', 'grouped')
            os.makedirs(PLOT_DIR, exist_ok=True)
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{key_size}_signing_verification_matplotlib.png')

            # Save the plot
            plt.savefig(PLOT_PATH)

            # Show the plot
            plt.show()

        # Create the grouped bar chart for encryption and decryption (if applicable)
        if algorithm in ['RSA']:
            plt.figure(figsize=(10, 6))
            if not df[df['operation'] == 'encryption'].empty:
                plt.bar(x, df[df['operation'] == 'encryption']['time_taken'],
                        width=bar_width, label='Encryption', color='blue')
            if not df[df['operation'] == 'decryption'].empty:
                plt.bar([p + bar_width for p in x], df[df['operation'] == 'decryption']['time_taken'],
                        width=bar_width, label='Decryption', color='green')
            plt.xticks([p + bar_width for p in x], df['file_size'].unique())

            # Set labels and title
            plt.xlabel('File Size')
            plt.ylabel('Time Taken (seconds)')
            plt.title(f'{algorithm} Encryption and Decryption Time vs. File Size (Key Size: {key_size})')
            plt.xticks(rotation=45)
            plt.legend()

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{key_size}_encryption_decryption_matplotlib.png')

            # Save the plot
            plt.savefig(PLOT_PATH)

            # Show the plot
            plt.show()

        # Create the grouped bar chart for key exchange (if applicable)
        if algorithm == 'DH':
            plt.figure(figsize=(10, 6))
            if not df[df['operation'] == 'key_exchange'].empty:
                plt.bar(x, df[df['operation'] == 'key_exchange']['time_taken'],
                        width=bar_width, label='Key Exchange', color='purple')
            plt.xticks([p + bar_width for p in x], df['file_size'].unique())

            # Set labels and title
            plt.xlabel('File Size')
            plt.ylabel('Time Taken (seconds)')
            plt.title(f'{algorithm} Key Exchange Time vs. File Size (Key Size: {key_size})')
            plt.xticks(rotation=45)
            plt.legend()

            # Define the path to save the plot
            PLOT_PATH = os.path.join(PLOT_DIR, f'{algorithm}_{key_size}_key_exchange_matplotlib.png')

            # Save the plot
            plt.savefig(PLOT_PATH)

            # Show the plot
            plt.show()
