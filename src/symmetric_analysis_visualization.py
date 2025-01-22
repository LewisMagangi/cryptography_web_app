import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the performance CSV file
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'symmetric_analysis_results.csv')

class SymmetricDataVisualization:
    def __init__(self):
        self.data = pd.read_csv(RESULTS_PATH)
        self.algorithms = ["AES", "DES", "3DES", "Blowfish", "RC4", "RC2"]
        self.base_plot_dir = os.path.join(os.path.dirname(__file__), '..', 'media', 'plots', 'symmetric_analysis')
        os.makedirs(self.base_plot_dir, exist_ok=True)
        self.colors = {
            "AES": "blue",
            "DES": "green",
            "3DES": "red",
            "RC2": "purple",
            "RC4": "orange",
            "Blowfish": "brown"
        }
        self.operation_colors = {
            "encryption": "blue",
            "decryption": "green",
        }

    def clean_file_name(self, file_name):
        """Extract and clean the data size from the file name."""
        return file_name.split('_')[0]

    def plot_time_graphs(self):
        """
        Plot graphs showing the relation of time taken for each operation.
        """
        operations = self.data['operation'].unique()
        for operation in operations:
            plt.figure(figsize=(10, 6))
            for algo in self.algorithms:
                algo_data = self.data[(self.data['algorithm'] == algo) & (self.data['operation'] == operation)]
                plt.plot(algo_data['key_size'], algo_data['time_taken'], label=algo, color=self.colors[algo])

            plt.title(f"Time Analysis for {operation.capitalize()} Operation")
            plt.xlabel("Key Size")
            plt.ylabel("Time Taken (seconds)")
            plt.legend()
            plt.grid(True)

            # Save the plot
            plot_dir = os.path.join(self.base_plot_dir, 'time')
            os.makedirs(plot_dir, exist_ok=True)
            plot_filename = f"time_analysis_{operation}.png"
            plt.savefig(os.path.join(plot_dir, plot_filename))
            plt.close()

    def plot_keysize_graphs(self):
        """
        Plot graphs showing the relation of key size for each algorithm with different data sizes.
        """
        for algo in self.algorithms:
            algo_data = self.data[self.data['algorithm'] == algo]
            for file_name in algo_data['file_name'].unique():
                plt.figure(figsize=(10, 6))
                file_data = algo_data[algo_data['file_name'] == file_name]
                for operation in file_data['operation'].unique():
                    operation_data = file_data[file_data['operation'] == operation]
                    plt.plot(operation_data['key_size'], operation_data['time_taken'], label=operation, color=self.operation_colors[operation])

                plt.title(f"Key Size Analysis for {algo} Algorithm ({self.clean_file_name(file_name)})")
                plt.xlabel("Key Size")
                plt.ylabel("Time Taken (seconds)")
                plt.legend()
                plt.grid(True)

                # Save the plot
                plot_dir = os.path.join(self.base_plot_dir, 'keysize')
                os.makedirs(plot_dir, exist_ok=True)
                plot_filename = f"keysize_analysis_{algo}_{self.clean_file_name(file_name)}.png"
                plt.savefig(os.path.join(plot_dir, plot_filename))
                plt.close()

    def plot_individual_operation_graphs(self):
        """
        Plot graphs showing the relation of time taken for each operation for individual algorithms with different data sizes.
        """
        for algo in self.algorithms:
            algo_data = self.data[self.data['algorithm'] == algo]
            for operation in algo_data['operation'].unique():
                plt.figure(figsize=(10, 6))
                operation_data = algo_data[algo_data['operation'] == operation]
                for file_name in operation_data['file_name'].unique():
                    file_data = operation_data[operation_data['file_name'] == file_name]
                    plt.plot(file_data['key_size'], file_data['time_taken'], label=self.clean_file_name(file_name), color=self.operation_colors[operation])

                plt.title(f"{algo} {operation.capitalize()} Time Analysis with Different Data Sizes")
                plt.xlabel("Key Size")
                plt.ylabel("Time Taken (seconds)")
                plt.legend()
                plt.grid(True)

                # Save the plot
                plot_dir = os.path.join(self.base_plot_dir, 'individual_operations', algo.lower())
                os.makedirs(plot_dir, exist_ok=True)
                plot_filename = f"{algo}_{operation}_time_analysis.png"
                plt.savefig(os.path.join(plot_dir, plot_filename))
                plt.close()

    def plot_individual_algorithm_time_analysis(self):
        """
        Plot bar graphs showing the time analysis for individual algorithms with different data sizes.
        """
        for algo in self.algorithms:
            algo_data = self.data[self.data['algorithm'] == algo]
            for key_size in algo_data['key_size'].unique():
                plt.figure(figsize=(10, 6))
                key_data = algo_data[algo_data['key_size'] == key_size]
                key_data = key_data.sort_values(by='file_name', key=lambda x: x.str.extract(r'(\d+)').squeeze().astype(int))
                for operation in key_data['operation'].unique():
                    operation_data = key_data[key_data['operation'] == operation]
                    plt.bar(operation_data['file_name'].apply(self.clean_file_name), operation_data['time_taken'], label=operation, color=self.operation_colors[operation])

                plt.title(f"{algo} Time Analysis for Different Data Sizes (Key Size: {key_size})")
                plt.xlabel("Data Size")
                plt.ylabel("Time Taken (seconds)")
                plt.legend()
                plt.grid(True)

                # Save the plot
                plot_dir = os.path.join(self.base_plot_dir, 'individual_algorithms', algo.lower())
                os.makedirs(plot_dir, exist_ok=True)
                plot_filename = f"{algo}_time_analysis_keysize_{key_size}.png"
                plt.savefig(os.path.join(plot_dir, plot_filename))
                plt.close()

    def generate_all_plots(self):
        """
        Generate and save all plots.
        """
        self.plot_time_graphs()
        self.plot_keysize_graphs()
        self.plot_individual_operation_graphs()
        self.plot_individual_algorithm_time_analysis()

# Example usage
if __name__ == "__main__":
    # Create SymmetricDataVisualization instance
    visualizer = SymmetricDataVisualization()

    # Generate all plots
    visualizer.generate_all_plots()
