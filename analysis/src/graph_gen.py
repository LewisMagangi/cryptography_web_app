import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from plotly.offline import plot
from .time_gen import AsymmetricTimeCalculator, SymmetricTimeCalculator, HashingTimeCalculator 
import pandas as pd  # Add this import if format_table uses pandas

class GraphGenerator:
    def __init__(self, calculator):
        self.calculator = calculator

    def generate_graph_data(self, algorithm, file_size):
        """Main entry point for generating visualizations"""
        if isinstance(self.calculator, HashingTimeCalculator):
            return self.generate_hash_csv_display(algorithm)
        return self.generate_csv_display(algorithm, file_size)

    def generate_csv_display(self, algorithm, file_size):
        """Generate standard performance display for symmetric/asymmetric"""
        results = self.calculator.get_time_results(algorithm, file_size)  # Pass raw file size
        
        html = """
        <div class="performance-analysis">
            <h4>Basic Operation Performance</h4>
            <table class="table table-striped mb-4">
                <thead>
                    <tr>
                        <th>Operation</th>
                        <th>Time (s)</th>
                        <th>Rate (MB/s)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for op, result in results.items():
            html += f"""
                <tr class="performance-row">
                    <td>{op.title()}</td>
                    <td class="time-cell">{result['estimated_time']:.4f}</td>
                    <td class="rate-cell">{result['rate']:.2f}</td>
                </tr>
            """
            
        html += """
                </tbody>
            </table>
        """
        
        # Add interval analysis for symmetric algorithms
        if isinstance(self.calculator, SymmetricTimeCalculator):
            encryption_result = results['encryption']
            if 'intervals' in encryption_result:
                file_size_mb = file_size / 1024  # Convert KB to MB
                html += f"""
                <h4>Size-based Performance Analysis</h4>
                <p>Input File Size: {file_size_mb:.2f} MB</p>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>File Size (MB)</th>
                            <th>Estimated Time (s)</th>
                            <th>Rate (MB/s)</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                # Highlight row for actual file size
                for interval in encryption_result['intervals']:
                    is_current = abs(interval['size_mb'] - file_size_mb) < 0.01
                    row_class = 'table-primary' if is_current else 'performance-row'
                    html += f"""
                        <tr class="{row_class}">
                            <td>{interval['size_mb']:.2f}</td>
                            <td class="time-cell">{interval['estimated_time']:.4f}</td>
                            <td class="rate-cell">{interval['rate']:.2f}</td>
                        </tr>
                    """
                
                html += """
                    </tbody>
                </table>
                """
        
        html += "</div>"
        return html

    def generate_hash_csv_display(self, algorithm):
        """Generate hash performance display with intervals"""
        analysis = self.calculator.hash_data[
            self.calculator.hash_data['algorithm'].str.upper() == algorithm.upper()
        ]
        
        # Get actual file size from request
        file_size_kb = 10290.62  # This will be dynamic from the analysis
        file_size_mb = file_size_kb / 1024
        
        # Get rate for this algorithm
        rate = self.calculator.rates.get(algorithm.upper(), 0)
        
        # Calculate intervals based on actual file size
        base_size = file_size_mb
        intervals = [
            base_size * 0.4,  # 40% of file size
            base_size * 0.6,  # 60% of file size
            base_size * 0.8,  # 80% of file size
            base_size,        # 100% (actual size)
            base_size * 1.2,  # 120% of file size
            base_size * 1.4,  # 140% of file size
            base_size * 1.6   # 160% of file size
        ]
        
        html = """
        <div class="hash-analysis">
            <h5>Hash Performance Analysis</h5>
            <div class="summary mb-3">
                <p><strong>Average Processing Rate:</strong> {:.2f} MB/s</p>
            </div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>File Size (MB)</th>
                        <th>Estimated Time (s)</th>
                        <th>Rate (MB/s)</th>
                    </tr>
                </thead>
                <tbody>
        """.format(rate)
        
        for size in intervals:
            estimated_time = size / rate if rate > 0 else 0
            html += f"""
                <tr class="performance-row">
                    <td>{size:.2f}</td>
                    <td class="time-cell">{estimated_time:.4f}</td>
                    <td class="rate-cell">{rate:.2f}</td>
                </tr>
            """
            
        html += """
                </tbody>
            </table>
        </div>
        """
        return html