import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Define the path to the performance CSV file
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'symmetric_analysis_results.csv')

class SymmetricAnalysisVisualization:
    def __init__(self, data_path, base_plot_dir):
        self.data_path = data_path
        self.base_plot_dir = base_plot_dir
        self.data = pd.read_csv(data_path)
        self.algorithms = self.data['algorithm'].unique()
        self.operation_colors = {
            'encryption': 'blue',
            'decryption': 'red'
        }

    def clean_file_name(self, file_name):
        return file_name.replace('_', ' ').title()

    def plot_individual_algorithm_time_analysis(self):
        for algo in self.algorithms:
            algo_data = self.data[self.data['algorithm'] == algo]
            for key_size in algo_data['key_size'].unique():
                plt.figure(figsize=(10, 6))
                key_data = algo_data[algo_data['key_size'] == key_size]
                # Add your plotting code here

    def plot_grouped_bar_chart(self):
        fig_grouped = px.bar(self.data, 
                             x="algorithm", 
                             y="time_taken", 
                             color="operation", 
                             barmode="group",
                             facet_col="key_size",
                             title="Grouped Bar Chart: Encryption vs Decryption Time")
        plot_dir = os.path.join(self.base_plot_dir, 'barchart', 'grouped')
        os.makedirs(plot_dir, exist_ok=True)
        fig_grouped.write_image(os.path.join(plot_dir, "grouped_bar_chart.png"))

    def plot_stacked_bar_chart(self):
        fig_stacked = px.bar(self.data, 
                             x="algorithm", 
                             y="time_taken", 
                             color="operation", 
                             barmode="stack",
                             title="Stacked Bar Chart: Total Encryption & Decryption Time per Algorithm")
        plot_dir = os.path.join(self.base_plot_dir, 'barchart', 'stacked')
        os.makedirs(plot_dir, exist_ok=True)
        fig_stacked.write_image(os.path.join(plot_dir, "stacked_bar_chart.png"))

    def plot_multi_variable_bar_chart(self):
        fig_multi = px.bar(self.data, 
                           x="algorithm", 
                           y="time_taken", 
                           color="key_size", 
                           barmode="group",
                           facet_row="operation",
                           title="Multi-Variable Bar Chart: Key Size Comparison")
        plot_dir = os.path.join(self.base_plot_dir, 'barchart', 'multivariable')
        os.makedirs(plot_dir, exist_ok=True)
        fig_multi.write_image(os.path.join(plot_dir, "multi_variable_bar_chart.png"))

    def plot_blowfish_grouped_bar_chart(self):
        key_sizes = [4, 8, 16, 24, 32]
        blowfish_data = self.data[(self.data['algorithm'] == 'Blowfish') & (self.data['file_name'] == '50MB') & (self.data['key_size'].isin(key_sizes))]
        blowfish_data = blowfish_data.sort_values(by='key_size')

        # Separate data for encryption and decryption
        encryption_data = blowfish_data[blowfish_data['operation'] == 'encryption']
        decryption_data = blowfish_data[blowfish_data['operation'] == 'decryption']

        fig_blowfish = go.Figure(data=[
            go.Bar(name='Encryption', x=encryption_data['key_size'], y=encryption_data['time_taken'], marker=dict(color='blue')),
            go.Bar(name='Decryption', x=decryption_data['key_size'], y=decryption_data['time_taken'], marker=dict(color='red'))
        ])

        # Change the bar mode
        fig_blowfish.update_layout(
            barmode='group',
            title="Blowfish Grouped Bar Chart: Encryption vs Decryption Time for 50MB File",
            xaxis_title="Key Size",
            yaxis_title="Time Taken (seconds)",
            template="plotly_white" 
        )

        plot_dir = os.path.join(self.base_plot_dir, 'barchart', 'grouped')
        os.makedirs(plot_dir, exist_ok=True)
        fig_blowfish.write_image(os.path.join(plot_dir, "blowfish_grouped_bar_chart.svg"))

    def generate_all_plots(self):
        self.plot_individual_algorithm_time_analysis()
        self.plot_grouped_bar_chart()
        self.plot_stacked_bar_chart()
        self.plot_multi_variable_bar_chart()
        self.plot_blowfish_grouped_bar_chart()
        print("All charts saved successfully!")

# Define paths
PATH = RESULTS_PATH  # Path to the CSV file
RESULT_PATH = os.path.join(os.path.dirname(__file__), '..', 'media', 'plots', 'symmetric_analysis')  # Base directory to save charts

# Create an instance of the visualization class and generate all plots
visualization = SymmetricAnalysisVisualization(PATH, RESULT_PATH)
visualization.generate_all_plots()