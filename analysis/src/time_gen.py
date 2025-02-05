import os
import pandas as pd

class SymmetricTimeCalculator:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_path = os.path.join(project_root, 'analysis', 'data', 'results')
        self.sym_data = pd.read_csv(os.path.join(self.base_path, 'symmetric_analysis_results.csv'))
        self.rates = self.get_rates()

    def get_rates(self):
        """Extract rates from CSV data for all operations."""
        rates = {}
        operations = ['encryption', 'decryption']
        
        for _, row in self.sym_data.iterrows():
            alg = row['algorithm'].upper()
            op = row['operation']
            if op in operations:
                if alg not in rates:
                    rates[alg] = {}
                rates[alg][op] = row['rate']
        return rates

    def calculate_time(self, algorithm, file_size_kb, operation='encryption'):
        """Calculate time using rate from CSV."""
        algorithm = algorithm.upper()
        if algorithm == 'BLOWFISH':
            algorithm = 'Blowfish'
            
        file_size_mb = file_size_kb / 1024  # Convert KB to MB
        rate = self.rates.get(algorithm, {}).get(operation, 0)
        estimated_time = file_size_mb / rate if rate > 0 else 0
        
        # Calculate realistic intervals based on file size
        if file_size_mb < 1:
            base = 1  # Use 1MB as base for small files
        else:
            base = file_size_mb
            
        intervals = [
            base * 0.4,    # 40% of base
            base * 0.6,    # 60% of base
            base * 0.8,    # 80% of base
            file_size_mb,  # Actual file size
            base * 1.2,    # 120% of base
            base * 1.4,    # 140% of base
            base * 1.6     # 160% of base
        ]
        
        interval_times = []
        for size in intervals:
            if size > 0:
                time = size / rate if rate > 0 else 0
                interval_times.append({
                    'size_mb': size,
                    'estimated_time': time,
                    'rate': rate
                })
        
        return {
            'algorithm': algorithm,
            'file_size_kb': file_size_kb,
            'operation': operation,
            'estimated_time': estimated_time,
            'rate': rate,
            'intervals': interval_times
        }

    def get_file_details(self, algorithm, file_size):
        """Get file details structure"""
        return {
            'algorithm': algorithm.upper(),
            'file_size': file_size,
            'type': 'symmetric'
        }

    def get_time_results(self, algorithm, file_size_kb):
        """Get time results for both operations"""
        return {
            'encryption': self.calculate_time(algorithm, file_size_kb, 'encryption'),
            'decryption': self.calculate_time(algorithm, file_size_kb, 'decryption')
        }

class AsymmetricTimeCalculator:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_path = os.path.join(project_root, 'analysis', 'data', 'results')
        self.asym_data = pd.read_csv(os.path.join(self.base_path, 'asymmetric_analysis_results.csv'))
        self.rates = self.get_rates()

    def get_rates(self):
        """Extract rates from CSV data for all operations."""
        rates = {}
        operations = ['encryption', 'decryption', 'signing', 'verification', 'key_exchange']
        
        for _, row in self.asym_data.iterrows():
            alg = row['algorithm'].upper()
            op = row['operation']
            if op in operations:
                if alg not in rates:
                    rates[alg] = {}
                rates[alg][op] = row['rate']
        return rates

    def calculate_time(self, algorithm, file_size_kb, operation='encryption'):
        """Calculate time using rate from CSV."""
        algorithm = algorithm.upper()
        if algorithm == 'ECDSA':
            algorithm = 'ECC'
            
        file_size_bytes = file_size_kb * 1024  # Convert KB to bytes
        rate = self.rates.get(algorithm, {}).get(operation, 0)
        estimated_time = file_size_bytes / rate if rate > 0 else 0
        
        return {
            'algorithm': algorithm,
            'file_size_kb': file_size_kb,
            'operation': operation,
            'estimated_time': estimated_time,
            'rate': rate
        }

    def get_file_details(self, algorithm, file_size):
        """Get file details structure"""
        return {
            'algorithm': algorithm.upper(),
            'file_size': file_size,
            'type': 'asymmetric'
        }

    def get_time_results(self, algorithm, file_size_kb):
        """Get time results for both operations"""
        return {
            'encryption': self.calculate_time(algorithm, file_size_kb, 'encryption'),
            'decryption': self.calculate_time(algorithm, file_size_kb, 'decryption')
        }

class HashingTimeCalculator:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_path = os.path.join(project_root, 'analysis', 'data', 'results')
        self.hash_data = pd.read_csv(os.path.join(self.base_path, 'hashing_analysis_results.csv'))
        # Convert column names to lowercase for consistency
        self.hash_data.columns = self.hash_data.columns.str.lower()
        self.rates = self.get_rates()

    def get_rates(self):
        """Calculate mean rate for each algorithm across all file sizes"""
        rates = {}
        grouped = self.hash_data.groupby('algorithm').agg({
            'time_taken': 'mean',
            'file_name': lambda x: [float(fn.split('mb_')[0]) for fn in x]
        })
        
        for alg, row in grouped.iterrows():
            avg_file_size = sum(row['file_name']) / len(row['file_name'])
            mean_rate = avg_file_size / row['time_taken'] if row['time_taken'] > 0 else 0
            rates[alg.upper()] = mean_rate
        
        return rates

    def calculate_time(self, algorithm, file_size_kb, operation=None):
        """Calculate time using mean rate from CSV."""
        algorithm = algorithm.upper().replace('-', '')  # Normalize algorithm name
        file_size_mb = file_size_kb / 1024  # Convert KB to MB
        
        # Map normalized names to CSV names
        algo_map = {
            'SHA1': 'SHA-1',
            'SHA224': 'SHA-224',
            'SHA256': 'SHA-256',
            'SHA384': 'SHA-384',
            'SHA512': 'SHA-512'
        }
        
        lookup_name = algo_map.get(algorithm, algorithm)
        rate = self.rates.get(lookup_name, 0)
        estimated_time = file_size_mb / rate if rate > 0 else 0
        
        # Calculate intervals based on actual file size
        base_interval = file_size_mb / 5
        sizes = []
        
        # Ensure we have the actual file size in our intervals
        if file_size_mb > 0:
            sizes = [
                file_size_mb * 0.4,  # 40% of file size
                file_size_mb * 0.6,  # 60% of file size
                file_size_mb * 0.8,  # 80% of file size
                file_size_mb,        # 100% (actual size)
                file_size_mb * 1.2,  # 120% of file size
                file_size_mb * 1.4,  # 140% of file size
                file_size_mb * 1.6   # 160% of file size
            ]
        
        # Calculate times for each interval
        interval_times = []
        for size in sizes:
            time = size / rate if rate > 0 else 0
            interval_times.append({
                'size_mb': size,
                'estimated_time': time,
                'rate': rate
            })
        
        return {
            'algorithm': lookup_name,
            'file_size_kb': file_size_kb,
            'operation': 'hashing',
            'estimated_time': estimated_time,
            'rate': rate,
            'intervals': interval_times
        }

    def get_time_results(self, algorithm, file_size_kb):
        """Get time results with intervals"""
        result = self.calculate_time(algorithm, file_size_kb)
        return {
            'hashing': result
        }
