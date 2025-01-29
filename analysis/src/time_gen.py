import pandas as pd
import os

class SymmetricTimeCalculator:
    def __init__(self):
        self.base_path = 'analysis/data/results'
        self.sym_data = pd.read_csv(os.path.join(self.base_path, 'symmetric_analysis_results.csv'))
        self.calculate_rates()

    def calculate_rates(self):
        # Group by algorithm and operation, calculate rate per MB
        grouped_data = self.sym_data.groupby(['algorithm', 'operation']).apply(
            lambda x: x['time_taken'].mean() / (50)  # Rate per MB (using 50MB baseline)
        ).to_dict()
        
        self.rates = {
            'AES': {'encryption': grouped_data[('AES', 'encryption')], 'decryption': grouped_data[('AES', 'decryption')]},
            'DES': {'encryption': grouped_data[('DES', 'encryption')], 'decryption': grouped_data[('DES', 'decryption')]},
            '3DES': {'encryption': grouped_data[('3DES', 'encryption')], 'decryption': grouped_data[('3DES', 'decryption')]},
            'RC2': {'encryption': grouped_data[('RC2', 'encryption')], 'decryption': grouped_data[('RC2', 'decryption')]},
            'RC4': {'encryption': grouped_data[('RC4', 'encryption')], 'decryption': grouped_data[('RC4', 'decryption')]},
            'BLOWFISH': {'encryption': grouped_data[('Blowfish', 'encryption')], 'decryption': grouped_data[('Blowfish', 'decryption')]}
        }

    def get_rate(self, algorithm, operation='encryption'):
        # Convert algorithm to uppercase to match stored rates
        algorithm = algorithm.upper()
        if algorithm == 'BLOWFISH':
            algorithm = 'Blowfish'  # Special case for Blowfish
        return self.rates[operation][algorithm]

    def calculate_time(self, algorithm, file_size_kb, operation='encryption'):
        algorithm = algorithm.upper()
        if algorithm == 'BLOWFISH':
            algorithm = 'BLOWFISH'
            
        # Convert KB to MB for calculation
        file_size_mb = file_size_kb / 1024
        rate = self.rates[algorithm][operation]
        estimated_time = file_size_mb * rate  # Time in seconds
        
        return {
            'algorithm': algorithm,
            'file_size_kb': file_size_kb,
            'operation': operation,
            'estimated_time': estimated_time,
            'rate': rate
        }

class AsymmetricTimeCalculator:
    pass

class HashingTimeCalculator:
    pass