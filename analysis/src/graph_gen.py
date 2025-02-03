from .time_gen import AsymmetricTimeCalculator, SymmetricTimeCalculator, HashingTimeCalculator 
import pandas as pd  # Add this import if format_table uses pandas

class GraphGenerator:
    def __init__(self, calculator):
        self.calculator = calculator

    def generate_graph_data(self, algorithm, file_size):
        """Generate graph data for given algorithm and file size"""
        file_details = self.calculator.get_file_details(algorithm, file_size)
        time_results = self.calculator.get_time_results(algorithm, file_size/1024)  # Convert to KB
        return self.generate_csv_display(file_details, time_results)

    def generate_csv_display(self, file_details, time_results):
        # Calculate intervals from input file size
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
        
        # Generate data for each size
        data = []
        for size in sizes:
            enc_result = self.calculator.calculate_time(
                algorithm=file_details['algorithm'],
                file_size_kb=size/1024,  # Convert bytes to KB
                operation='encryption'
            )
            dec_result = self.calculator.calculate_time(
                algorithm=file_details['algorithm'],
                file_size_kb=size/1024,
                operation='decryption'
            )
            
            data.append({
                'size': f"{size/1024/1024:.1f}MB",  # Convert to MB for display
                'encryption': {
                    'rate': f"{enc_result['rate']:.2f}",
                    'time': f"{enc_result['estimated_time']:.4f}"
                },
                'decryption': {
                    'rate': f"{dec_result['rate']:.2f}",
                    'time': f"{dec_result['estimated_time']:.4f}"
                }
            })
        
        return self.format_table(data)
    
    def format_table(self, data):
        """Format data as an HTML table."""
        df = pd.DataFrame(data)
        return df.to_html(index=False)