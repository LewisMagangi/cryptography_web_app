import os
import psutil
import time
import pandas as pd

# Import specific algorithms directly
from src.symmetric import AESEncryption, DESEncryption, DES3Encryption, RC2Encryption, RC4Encryption, BlowfishEncryption
from src.asymmetric import RSAEncryption, DSAEncryption, DHEncryption, ECCEncryption
from src.hashing import SHA1Hash, SHA2Hash, MD5Hash, HMACHash

# Define constants
DATA_DIR = "./data/sample_text" 
RESULTS_PATH = "./data/results/performance_data.csv" 
DEFAULT_ITERATIONS = 10 
DEFAULT_KEYSIZE = 256  

class PerformanceMetrics:
    """Class to calculate and store performance metrics."""

    def __init__(self, iterations=DEFAULT_ITERATIONS):
        """
        Initialize the PerformanceMetrics object.

        Args:
            iterations (int): Number of iterations to measure performance over.
        """
        self.iterations = iterations
        self.total_time = 0
        self.total_cpu = 0
        self.total_ram = 0

    def record_iteration(self, start_time, start_cpu, start_ram):
        """
        Record performance metrics for a single iteration.

        Args:
            start_time (float): Start time of the iteration.
            start_cpu (float): CPU usage percentage at the start.
            start_ram (float): RAM usage percentage at the start.
        """
        end_time = time.time()
        end_cpu = psutil.cpu_percent(interval=None)
        end_ram = psutil.virtual_memory().percent

        self.total_time += (end_time - start_time)
        self.total_cpu += (end_cpu - start_cpu)
        self.total_ram += (end_ram - start_ram)

    def get_averages(self):
        """
        Calculate average metrics over all iterations.

        Returns:
            dict: A dictionary containing average time, CPU usage, and RAM usage.
        """
        return {
            "avg_time": self.total_time / self.iterations,
            "avg_cpu": self.total_cpu / self.iterations,
            "avg_ram": self.total_ram / self.iterations,
        }


class PerformanceAnalyzer:
    """Class to manage the performance analysis process."""

    def __init__(self, data_dir=DATA_DIR, results_path=RESULTS_PATH):
        """
        Initialize the PerformanceAnalyzer object.

        Args:
            data_dir (str): Path to the directory containing data files.
            results_path (str): Path to the CSV file for saving results.
        """
        self.data_dir = data_dir
        self.results_path = results_path
        self.algorithms = {
            "AESEncryption": AESEncryption,
            "DESEncryption": DESEncryption,
            "DES3Encryption": DES3Encryption,
            "RC2Encryption": RC2Encryption,
            "RC4Encryption": RC4Encryption,
            "BlowfishEncryption": BlowfishEncryption,
            "RSAEncryption": RSAEncryption,
            "DSAEncryption": DSAEncryption,
            "DHEncryption": DHEncryption,
            "ECCEncryption": ECCEncryption,
            "SHA1Hash": SHA1Hash,
            "SHA2Hash": SHA2Hash,
            "MD5Hash": MD5Hash,
            "HMACHash": HMACHash,
        }

    def get_data_files(self):
        """
        Fetch all text files from the data directory.

        Returns:
            list: A list of file paths for data files in the data directory.
        """
        return [os.path.join(self.data_dir, file) for file in os.listdir(self.data_dir) if file.endswith(".txt")]

    def analyze_algorithm(self, algo_name, algo_class, data, key_size=None):
        """
        Analyze the performance of a specific algorithm with given data.

        Args:
            algo_name (str): Name of the algorithm.
            algo_class (class): The class representing the algorithm.
            data (bytes): The input data to process.
            key_size (int): The key size for encryption algorithms.

        Returns:
            dict: A dictionary containing average performance metrics.
        """
        metrics = PerformanceMetrics()
        for _ in range(metrics.iterations):
            start_time = time.time()
            start_cpu = psutil.cpu_percent(interval=None)
            start_ram = psutil.virtual_memory().percent

            # Execute algorithm function
            algo_instance = algo_class(key_size) if key_size else algo_class()
            if "Encryption" in algo_name:
                encrypted_data = algo_instance.encrypt(data)
            elif "Hash" in algo_name:
                hashed_data = algo_instance.hash(data)

            metrics.record_iteration(start_time, start_cpu, start_ram)

        return metrics.get_averages()

    def save_results(self, results):
        """
        Save the results to a CSV file, updating existing entries if needed.

        Args:
            results (list): A list of dictionaries containing performance results.
        """
        if os.path.exists(self.results_path):
            df = pd.read_csv(self.results_path)
        else:
            df = pd.DataFrame(columns=["algorithm", "data_size", "iterations", "key_size", "avg_time", "avg_cpu", "avg_ram"])

        for result in results:
            # Update existing entries or append new ones
            mask = (
                (df["algorithm"] == result["algorithm"]) &
                (df["data_size"] == result["data_size"]) &
                (df["iterations"] == result["iterations"]) &
                (df["key_size"] == result["key_size"])
            )
            if mask.any():
                df.loc[mask, ["avg_time", "avg_cpu", "avg_ram"]] = [
                    result["avg_time"], result["avg_cpu"], result["avg_ram"]
                ]
            else:
                df = df.append(result, ignore_index=True)

        df.to_csv(self.results_path, index=False)

    def analyze_performance(self, iterations=DEFAULT_ITERATIONS, key_size=DEFAULT_KEYSIZE):
        """
        Perform the full performance analysis.

        Args:
            iterations (int): Number of iterations to measure performance.
            key_size (int): Key size for encryption algorithms.
        """
        data_files = self.get_data_files()  # Load data files
        results = []

        for algo_name, algo_class in self.algorithms.items():
            for data_path in data_files:
                with open(data_path, "rb") as file:
                    data = file.read()

                averages = self.analyze_algorithm(algo_name, algo_class, data, key_size)
                results.append({
                    "algorithm": algo_name,
                    "data_size": os.path.basename(data_path),
                    "iterations": iterations,
                    "key_size": key_size,
                    **averages,
                })

        self.save_results(results)


# Main execution
if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    analyzer.analyze_performance()
