from .time_gen import AsymmetricTimeCalculator, SymmetricTimeCalculator, HashingTimeCalculator
import numpy as np
from django.template.loader import render_to_string

class GraphGenerator:
    def __init__(self, calculator):
        self.calculator = calculator

    def _convert_to_float(self, value):
        """Convert numpy types to Python float."""
        if isinstance(value, (np.float64, np.float32, np.int64, np.int32)):
            return float(value)
        return value

    def _convert_dict_values(self, d):
        """Convert all numpy values in a dictionary to Python types."""
        if not isinstance(d, dict):
            return self._convert_to_float(d)
        return {k: self._convert_dict_values(v) for k, v in d.items()}

    def _format_size(self, size_bytes, include_all=False):
        """
        Convert bytes to appropriate unit with option to show all units.
        """
        if include_all:
            kb = size_bytes / 1024
            mb = kb / 1024
            return f"{size_bytes:.2f} B ({kb:.2f} KB, {mb:.6f} MB)"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"

    def _normalize_rate(self, rate, is_asymmetric=False):
        """Normalize processing rate to MB/s."""
        if is_asymmetric:
            # Convert from bytes/s to MB/s
            return rate / (1024 * 1024)
        return rate  # Symmetric rates are already in MB/s

    def generate_graph_data(self, algorithm, file_size):
        """Main entry point for generating visualizations"""
        if isinstance(self.calculator, HashingTimeCalculator):
            return self.generate_hash_csv_display(algorithm)
        return self.generate_csv_display(algorithm, file_size)

    def generate_csv_display(self, algorithm, file_size):
        """Generate performance display based on view type."""
        results = self.calculator.get_time_results(algorithm, file_size)
        results = self._convert_dict_values(results)
        
        # Normalize algorithm name
        algorithm = algorithm.upper()
        if algorithm == 'BLOWFISH':
            algorithm = 'Blowfish'  # Match the case in the data
            
        # Check if we have key size stats for this algorithm
        has_key_size_stats = any(
            result.get('key_size_stats') 
            for result in results.values() 
            if isinstance(result, dict)
        )
        
        if has_key_size_stats:
            return self.generate_keysize_analysis(algorithm, file_size)
        return self.generate_filesize_analysis(algorithm, file_size)

    def generate_keysize_analysis(self, algorithm, file_size):
        """Generate keysize-specific analysis."""
        results = self.calculator.get_time_results(algorithm, file_size)
        results = self._convert_dict_values(results)
        return self._generate_keysize_view(algorithm, results, file_size)

    def generate_filesize_analysis(self, algorithm, file_size):
        """Generate filesize-specific analysis."""
        results = self.calculator.get_time_results(algorithm, file_size)
        results = self._convert_dict_values(results)
        return self._generate_filesize_view(algorithm, file_size, results)

    def _generate_keysize_view(self, algorithm, results, file_size):
        """Generate view focusing on key size performance."""
        is_asymmetric = isinstance(self.calculator, AsymmetricTimeCalculator)
        file_size_bytes = file_size * 1024
        
        rows = []
        all_rates = []
        
        for op, result in results.items():
            if isinstance(result, dict):
                stats = result.get('key_size_stats', [])
                if isinstance(stats, (list, tuple)):
                    for stat in sorted(stats, key=lambda x: x.get('key_size', 0)):
                        if isinstance(stat, dict):
                            # Pass algorithm to _prepare_keysize_row
                            row_data = self._prepare_keysize_row(stat, op, file_size, is_asymmetric, algorithm)
                            rows.append(row_data)
                            all_rates.append(row_data['rate'])

        context = {
            'algorithm': algorithm,
            'file_size_bytes': file_size * 1024,
            'file_size_kb': file_size,
            'rows': rows,
            'average': self._calculate_average(all_rates, file_size, is_asymmetric) if all_rates else None,
            'template_name': 'keysize_template'  # Add template name
        }
        
        return render_to_string('analysis/layouts/performance_templates.html', context)

    def _generate_filesize_view(self, algorithm, file_size, results):
        """Generate view focusing on file size performance."""
        file_size_bytes = file_size * 1024  # KB to bytes
        is_asymmetric = isinstance(self.calculator, AsymmetricTimeCalculator)
        
        rows = []
        for op, result in results.items():
            if isinstance(result, dict):
                row_data = self._prepare_filesize_row(result, op, file_size_bytes, is_asymmetric)
                rows.append(row_data)

        context = {
            'algorithm': algorithm,
            'size_display': self._format_size(file_size_bytes, True),
            'rows': sorted(rows, key=lambda x: x['operation']),  # Sort rows by operation
            'file_size_bytes': file_size_bytes,
            'file_size_mb': file_size / 1024
        }
        
        return render_to_string('analysis/filesize_analysis.html', context)

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
        base_intervals = [
            base_size * 0.4,  # 40% of file size
            base_size * 0.6,  # 60% of file size
            base_size * 0.8,  # 80% of file size
            base_size,        # 100% (actual size)
            base_size * 1.2,  # 120% of file size
            base_size * 1.4,  # 140% of file size
            base_size * 1.6   # 160% of file size
        ]
        
        intervals = []
        for size in base_intervals:
            intervals.append({
                'size': size,
                'time': size / rate if rate > 0 else 0,
                'rate': rate
            })

        context = {
            'avg_rate': rate,
            'intervals': intervals,
            'template_name': 'hash_template'  # Add template name
        }
        
        return render_to_string('analysis/layouts/performance_templates.html', context)

    def _prepare_keysize_row(self, stat, operation, file_size, is_asymmetric, algorithm):
        """Prepare row data for keysize analysis."""
        try:
            key_size = self._convert_to_float(stat.get('key_size', 0))
            rate = self._convert_to_float(stat.get('rate', 0))
            
            if is_asymmetric:
                # Convert bytes/s to MB/s for asymmetric
                mb_rate = rate / (1024 * 1024)
                file_size_bytes = file_size * 1024
                estimated_time = file_size_bytes / rate if rate > 0 else 0
            else:
                # For symmetric algorithms
                mb_rate = rate  # Already in MB/s
                file_size_mb = file_size / 1024
                estimated_time = file_size_mb / rate if rate > 0 else 0

            return {
                'key_size': key_size,
                'key_size_label': self._get_key_size_label(algorithm, key_size),
                'operation': operation,
                'estimated_time': estimated_time,
                'rate': mb_rate
            }
        except Exception as e:
            # Return safe default values if any calculation fails
            return {
                'key_size': 0,
                'key_size_label': 'Unknown',
                'operation': operation,
                'estimated_time': 0,
                'rate': 0
            }

    def _prepare_filesize_row(self, result, operation, file_size_bytes, is_asymmetric):
        """Prepare row data for filesize analysis."""
        raw_rate = self._convert_to_float(result.get('rate', 0))
        
        if is_asymmetric:
            # For asymmetric, rate is in bytes/s
            rate = raw_rate / (1024 * 1024)  # Convert to MB/s
            estimated_time = file_size_bytes / raw_rate if raw_rate > 0 else 0
        else:
            # For symmetric, rate is already in MB/s
            rate = raw_rate
            file_size_mb = file_size_bytes / (1024 * 1024)
            estimated_time = file_size_mb / rate if rate > 0 else 0

        return {
            'size_display': self._format_size(file_size_bytes),
            'operation': operation,
            'estimated_time': estimated_time,
            'rate': rate
        }

    def _calculate_average(self, rates, file_size, is_asymmetric):
        """Calculate average rate and time."""
        if not rates:
            return None
            
        avg_rate = sum(rates) / len(rates)
        
        if is_asymmetric:
            file_size_bytes = file_size * 1024
            avg_time = file_size_bytes / (avg_rate * 1024 * 1024) if avg_rate > 0 else 0
        else:
            file_size_mb = file_size / 1024
            avg_time = file_size_mb / avg_rate if avg_rate > 0 else 0
            
        return {
            'time': avg_time,
            'rate': avg_rate
        }

    def _get_key_size_label(self, algorithm, size):
        """Get formatted key size label."""
        size = self._convert_to_float(size)
        if algorithm.upper() == 'AES':
            return f"{int(size * 8)} bits (AES-{int(size * 8)})"
        elif algorithm.upper() in ['ECC', 'ECDSA']:
            return f"Curve {size}"
        return f"{int(size)} bits"