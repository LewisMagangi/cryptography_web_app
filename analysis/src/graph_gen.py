import plotly.express as px
import pandas as pd
import math

class GraphGenerator:
    def __init__(self, calculator):
        self.calculator = calculator

    def generate_plot(self, file_details, time_results):
        # Calculate intervals
        file_size = file_details['file_size']
        interval = int(file_size / 5)
        sizes = [
            max(0, file_size - 3*interval),
            max(0, file_size - 2*interval),
            max(0, file_size - interval),
            file_size,
            file_size + interval,
            file_size + 2*interval,
            file_size + 3*interval
        ]

        # Calculate times for each size
        data = []
        for size in sizes:
            enc_result = self.calculator.calculate_time(
                algorithm=file_details['algorithm'],
                file_size_kb=size,
                operation='encryption'
            )
            dec_result = self.calculator.calculate_time(
                algorithm=file_details['algorithm'],
                file_size_kb=size,
                operation='decryption'
            )
            data.extend([
                {'Size': size, 'Time': enc_result['estimated_time'], 'Operation': 'Encryption'},
                {'Size': size, 'Time': dec_result['estimated_time'], 'Operation': 'Decryption'}
            ])

        df = pd.DataFrame(data)
        
        fig = px.bar(df, 
                    x='Size', 
                    y='Time',
                    color='Operation',
                    barmode='group',
                    title=f"Performance Analysis for {file_details['file_name']}")
        
        return fig.to_html()