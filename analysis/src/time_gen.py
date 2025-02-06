import os
import pandas as pd

class SymmetricTimeCalculator:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_path = os.path.join(project_root, 'analysis', 'data', 'results')
        self.sym_data = pd.read_csv(os.path.join(self.base_path, 'symmetric_analysis_results.csv'))
        self.rates = self.get_rates()

    def get_rates(self):
        """Extract rates and calculate means per key size from CSV data."""
        rates = {}
        operations = ['encryption', 'decryption']
        
        # Group by algorithm and calculate mean rates for each key size
        for alg in self.sym_data['algorithm'].unique():
            alg_data = self.sym_data[self.sym_data['algorithm'] == alg]
            rates[alg.upper()] = {
                'key_size_means': {},
                'overall_mean': {}
            }
            
            # Calculate means for each key size
            for key_size in alg_data['key_size'].unique():
                key_data = alg_data[alg_data['key_size'] == key_size]
                rates[alg.upper()]['key_size_means'][key_size] = {
                    op: key_data[key_data['operation'] == op]['rate'].mean()
                    for op in operations
                }
            
            # Calculate overall mean across all key sizes
            for op in operations:
                rates[alg.upper()]['overall_mean'][op] = alg_data[alg_data['operation'] == op]['rate'].mean()
            
            # Special handling for Blowfish
            if alg.lower() == 'blowfish':
                rates['Blowfish'] = rates.pop('BLOWFISH')

        return rates

    def calculate_time(self, algorithm, file_size_kb, operation='encryption'):
        """Calculate time using mean rates from CSV."""
        algorithm = algorithm.upper()
        # Special case for Blowfish
        if algorithm.upper() == 'BLOWFISH':
            algorithm = 'Blowfish'
            
        file_size_mb = file_size_kb / 1024
        alg_rates = self.rates.get(algorithm, {})
        
        # Get both per-key-size and overall means
        key_size_means = alg_rates.get('key_size_means', {})
        overall_mean = alg_rates.get('overall_mean', {}).get(operation, 0)
        
        # For filesize analysis, use average rate across all key sizes
        intervals = []
        if overall_mean > 0:
            base_intervals = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
            for factor in base_intervals:
                size = file_size_mb * factor
                intervals.append({
                    'size_mb': size,
                    'estimated_time': size / overall_mean if overall_mean > 0 else 0,
                    'rate': overall_mean
                })

        return {
            'algorithm': algorithm,
            'file_size_kb': file_size_kb,
            'operation': operation,
            'estimated_time': file_size_mb / overall_mean if overall_mean > 0 else 0,
            'overall_rate': overall_mean,
            'key_size_stats': [
                {
                    'key_size': key_size,
                    'rate': rates.get(operation, 0),
                    'estimated_time': file_size_mb / rates.get(operation, 1) if rates.get(operation, 0) > 0 else 0
                }
                for key_size, rates in key_size_means.items()
            ],
            'intervals': intervals
        }

    def _get_keysize_analysis(self, algorithm, operation):
        """Get keysize-specific analysis with proper time estimation."""
        alg_rates = self.rates.get(algorithm, {})
        key_size_means = alg_rates.get('key_size_means', {})
        
        # Sample file sizes to estimate processing times (in MB)
        test_sizes = [1, 5, 10, 50, 100]  # 1MB to 100MB range
        
        # Prepare key size specific statistics
        key_size_stats = []
        for key_size, rates in key_size_means.items():
            rate = rates.get(operation, 0)
            if rate > 0:
                # Calculate average time for different file sizes
                times = []
                for size_mb in test_sizes:
                    process_time = size_mb / rate if rate > 0 else 0
                    times.append(process_time)
                
                # Use mean processing time
                avg_time = sum(times) / len(times)
                
                key_size_stats.append({
                    'key_size': key_size,
                    'rate': rate,
                    'estimated_time': avg_time,
                    'time_per_mb': 1 / rate if rate > 0 else 0,
                    'sample_times': {
                        f"{size}MB": size / rate if rate > 0 else 0
                        for size in test_sizes
                    }
                })
        
        # Calculate overall statistics
        overall_rate = alg_rates.get('overall_mean', {}).get(operation, 0)
        overall_times = {
            size: size / overall_rate if overall_rate > 0 else 0
            for size in test_sizes
        }
        
        return {
            'algorithm': algorithm,
            'file_size_kb': 0,
            'operation': operation,
            'estimated_time': sum(overall_times.values()) / len(overall_times),
            'overall_rate': overall_rate,
            'key_size_stats': sorted(key_size_stats, key=lambda x: x['key_size']),
            'sample_sizes': test_sizes,
            'overall_times': overall_times
        }

    def _calculate_intervals(self, file_size_mb, rate):
        """Calculate size intervals and their estimated times."""
        if file_size_mb < 1:
            base = 1
        else:
            base = file_size_mb
            
        intervals = [
            base * 0.4,
            base * 0.6,
            base * 0.8,
            file_size_mb,
            base * 1.2,
            base * 1.4,
            base * 1.6
        ]
        
        return [
            {
                'size_mb': size,
                'estimated_time': size / rate if rate > 0 else 0,
                'rate': rate
            }
            for size in intervals
        ]

    def get_file_details(self, algorithm, file_size):
        """Get file details structure"""
        return {
            'algorithm': algorithm.upper(),
            'file_size': file_size,
            'type': 'symmetric'
        }

    def get_time_results(self, algorithm, file_size_kb):
        """Get time results with detailed timing information."""
        algorithm = algorithm.upper()
        if algorithm == 'BLOWFISH':
            algorithm = 'Blowfish'

        # Filter data for specific algorithm
        alg_data = self.sym_data[self.sym_data['algorithm'] == algorithm]
        
        results = {}
        for operation in ['encryption', 'decryption']:
            op_data = alg_data[alg_data['operation'] == operation]
            
            if not op_data.empty:
                raw_rate = float(op_data['rate'].mean())  # Convert to float immediately
                
                # Add key size statistics
                key_size_stats = []
                for key_size in sorted(op_data['key_size'].unique()):
                    key_data = op_data[op_data['key_size'] == key_size]
                    if not key_data.empty:
                        rate = float(key_data['rate'].mean())  # Convert to float
                        if isinstance(rate, (int, float)) and rate > 1000:  # Type check before comparison
                            rate = rate / (1024 * 1024)
                        key_size_stats.append({
                            'key_size': float(key_size),  # Convert to float
                            'rate': rate
                        })
                
                # Calculate MB/s rate
                avg_rate = raw_rate
                if isinstance(avg_rate, (int, float)) and avg_rate > 1000:
                    avg_rate = avg_rate / (1024 * 1024)

                results[operation] = {
                    'rate': avg_rate,
                    'estimated_time': (file_size_kb / 1024) / avg_rate if avg_rate > 0 else 0,
                    'operation': operation,
                    'key_size_stats': sorted(key_size_stats, key=lambda x: float(x['key_size']))
                }

        return results

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
        """Get time results with detailed key size statistics."""
        algorithm = algorithm.upper()
        operations = ['encryption', 'decryption']
        if algorithm in ['RSA', 'DSA', 'ECC']:
            operations.extend(['signing', 'verification'])

        results = {}
        alg_data = self.asym_data[self.asym_data['algorithm'] == algorithm]
        
        for operation in operations:
            op_data = alg_data[alg_data['operation'] == operation]
            if not op_data.empty:
                # Calculate statistics per key size
                key_size_stats = []
                mean_rate = float(op_data['rate'].mean())  # Get mean rate for operation
                
                for key_size in sorted(op_data['key_size'].unique()):
                    key_data = op_data[op_data['key_size'] == key_size]
                    if not key_data.empty:
                        key_rate = float(key_data['rate'].mean())
                        key_size_stats.append({
                            'key_size': float(key_size),
                            'rate': key_rate
                        })

                results[operation] = {
                    'key_size_stats': key_size_stats,
                    'rate': mean_rate,  # Use mean rate directly
                    'estimated_time': (file_size_kb * 1024) / mean_rate if mean_rate > 0 else 0
                }

        return results

class HashingTimeCalculator:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_path = os.path.join(project_root, 'analysis', 'data', 'results')
        self.hash_data = pd.read_csv(os.path.join(self.base_path, 'hashing_analysis_results.csv'))
        self.rates = self.get_rates()

    def get_rates(self):
        """Calculate mean rate for each algorithm across all file sizes"""
        rates = {}
        grouped = self.hash_data.groupby('algorithm')['rate'].mean()
        return {alg.upper(): rate for alg, rate in grouped.items()}

    def get_time_results(self, algorithm, file_size_kb):
        """Get time results with intervals"""
        file_size_mb = file_size_kb / 1024
        rate = self.rates.get(algorithm.upper(), 0)
        
        # Calculate intervals
        intervals = []
        base_intervals = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
        for factor in base_intervals:
            size_mb = file_size_mb * factor
            intervals.append({
                'size_mb': size_mb,
                'time': size_mb / rate if rate > 0 else 0,
                'rate': rate
            })

        return {
            'hashing': {
                'rate': rate,
                'estimated_time': file_size_mb / rate if rate > 0 else 0,
                'intervals': intervals
            }
        }
