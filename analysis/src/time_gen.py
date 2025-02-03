import os
import pandas as pd

'''
algorithm,operation,key_size,file_name,time_taken,rate
AES,encryption,16,10mb_text_data_faker.txt,0.10004687309265137,99.95314886792318
AES,decryption,16,10mb_text_data_faker.txt,0.08319902420043945,120.19371736750706
AES,encryption,24,10mb_text_data_faker.txt,0.10018277168273926,99.81756176269703
AES,decryption,24,10mb_text_data_faker.txt,0.1071479320526123,93.32891273244313
AES,encryption,32,10mb_text_data_faker.txt,0.09465885162353516,105.64252395297058
AES,decryption,32,10mb_text_data_faker.txt,0.09807276725769043,101.96510488711478
DES,encryption,8,10mb_text_data_faker.txt,0.31646251678466797,31.59931893862914
DES,decryption,8,10mb_text_data_faker.txt,0.3167843818664551,31.567212818640918
3DES,encryption,16,10mb_text_data_faker.txt,0.735008716583252,13.605280827805439
3DES,decryption,16,10mb_text_data_faker.txt,0.8007967472076416,12.487563211101634
3DES,encryption,24,10mb_text_data_faker.txt,1.0478672981262207,9.54319312939896
3DES,decryption,24,10mb_text_data_faker.txt,1.3839678764343262,7.22560123704904
RC2,encryption,5,10mb_text_data_faker.txt,0.5225744247436523,19.136030250438445
RC2,decryption,5,10mb_text_data_faker.txt,0.34429335594177246,29.044998479991634
RC2,encryption,8,10mb_text_data_faker.txt,0.6248273849487305,16.004420166092014
RC2,decryption,8,10mb_text_data_faker.txt,0.34178829193115234,29.257877569470214
RC2,encryption,16,10mb_text_data_faker.txt,0.6152565479278564,16.25338248520774
RC2,decryption,16,10mb_text_data_faker.txt,0.3354666233062744,29.809224838651673
RC4,encryption,5,10mb_text_data_faker.txt,0.1482982635498047,67.43167290452855
RC4,decryption,5,10mb_text_data_faker.txt,0.17647600173950195,56.66492838363997
RC4,encryption,8,10mb_text_data_faker.txt,0.19018149375915527,52.581351646464306
RC4,decryption,8,10mb_text_data_faker.txt,0.15112686157226562,66.16957366786986
RC4,encryption,16,10mb_text_data_faker.txt,0.1499009132385254,66.71073433747395
'''
class SymmetricTimeCalculator:
    def __init__(self):
        self.base_path = 'analysis/data/results'
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
            
        file_size_mb = file_size_kb / 1024
        rate = self.rates.get(algorithm, {}).get(operation, 0)
        estimated_time = file_size_mb / rate if rate > 0 else 0
        
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
        self.base_path = 'analysis/data/results'
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
    pass