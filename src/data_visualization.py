import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the performance CSV file
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'performance_data.csv')

class DataVisualization:
    def __init__(self):
        self.data = pd.read_csv(RESULTS_PATH)
        self.algorithms = {
            "Symmetric": ["AESEncryption", "DESEncryption", "DES3Encryption", "RC2Encryption", "RC4Encryption", "BlowfishEncryption"],
            "Asymmetric": ["RSAEncryption", "DSAEncryption", "DHEncryption", "ECCEncryption"],
            "Hashing": ["SHA1Hash", "SHA2Hash", "MD5Hash", "HMACHash"]
        }
        self.base_plot_dir = os.path.join(os.path.dirname(__file__), '..', 'media', 'plots')
        os.makedirs(self.base_plot_dir, exist_ok=True)

    def clean_algorithm_name(self, name):
        """Clean algorithm name by removing suffixes."""
        return name.replace('Encryption', '').replace('Hash', '')

    def plot_line_graph(self, algo_type, metric):
        """
        Plot a line graph comparing performance metrics against data size for a given algorithm type.

        Args:
            algo_type (str): Type of algorithm (e.g., "Symmetric", "Asymmetric").
            metric (str): Performance metric to compare (e.g., "avg_cpu", "avg_ram", "avg_time").
        """
        if algo_type not in self.algorithms:
            print(f"Invalid algorithm type: {algo_type}")
            return

        filtered_data = self.data[self.data['algorithm'].isin(self.algorithms[algo_type])]

        plt.figure(figsize=(10, 6))
        for algo in self.algorithms[algo_type]:
            algo_data = filtered_data[filtered_data['algorithm'] == algo]
            algo_data = algo_data.sort_values(by='data_size', key=lambda x: x.str.extract(r'(\d+)').squeeze().astype(int))
            clean_name = self.clean_algorithm_name(algo)
            plt.plot(algo_data['data_size'].str.replace('_text_data_faker', ''), 
                    algo_data[metric], 
                    label=clean_name)

        plt.title(f"Comparison of {algo_type} Algorithms ({metric.replace('_', ' ').title()})")
        plt.xlabel("Data Size")
        plt.ylabel(metric.replace('_', ' ').title())
        plt.legend()
        plt.grid(True)

        # Save the plot with a descriptive name
        plot_dir = os.path.join(self.base_plot_dir, algo_type.lower())
        os.makedirs(plot_dir, exist_ok=True)
        plot_filename = f"{algo_type}_{metric}_comparison_line.png"
        plt.savefig(os.path.join(plot_dir, plot_filename))
        plt.close()

    def plot_bar_graph(self, algo_type, metric, data_size):
        """
        Plot a bar graph comparing performance metrics for algorithms of the same type at a specific data size.

        Args:
            algo_type (str): Type of algorithm (e.g., "Symmetric", "Asymmetric").
            metric (str): Performance metric to compare (e.g., "avg_cpu", "avg_ram", "avg_time").
            data_size (str): Specific data size to filter (e.g., "50MB").
        """
        if algo_type not in self.algorithms:
            print(f"Invalid algorithm type: {algo_type}")
            return

        filtered_data = self.data[(self.data['algorithm'].isin(self.algorithms[algo_type])) & 
                                (self.data['data_size'] == data_size)]

        if filtered_data.empty:
            print(f"No data available for {algo_type} algorithms with data size {data_size}.")
            return

        plt.figure(figsize=(10, 6))
        
        # Clean algorithm names for display
        labels = filtered_data['algorithm'].apply(self.clean_algorithm_name)
        plt.bar(labels, filtered_data[metric], color='skyblue')

        plt.title(f"{algo_type} Algorithms Performance at {data_size.replace('_text_data_faker', '')} ({metric.replace('_', ' ').title()})")
        plt.xlabel("Algorithm")
        plt.ylabel(metric.replace('_', ' ').title())
        plt.xticks(rotation=45)
        plt.grid(axis='y')

        # Save the plot with a descriptive name
        plot_dir = os.path.join(self.base_plot_dir, algo_type.lower())
        os.makedirs(plot_dir, exist_ok=True)
        plot_filename = f"{algo_type}_{metric}_{data_size}_comparison_bar.png"
        plt.savefig(os.path.join(plot_dir, plot_filename))
        plt.close()

    def generate_all_plots(self):
        """
        Generate and save plots for each algorithm type and each metric.
        """
        metrics = ['avg_cpu', 'avg_ram', 'avg_time']
        for algo_type in self.algorithms.keys():
            data_sizes = self.data[self.data['algorithm'].isin(self.algorithms[algo_type])]['data_size'].unique()
            for metric in metrics:
                self.plot_line_graph(algo_type, metric)
                for data_size in data_sizes:
                    self.plot_bar_graph(algo_type, metric, data_size)

# Example usage
if __name__ == "__main__":
    # Create DataVisualization instance
    visualizer = DataVisualization()

    # Generate all plots
    visualizer.generate_all_plots()