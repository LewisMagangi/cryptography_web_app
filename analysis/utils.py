def format_processing_data(file_size_kb, raw_rate, is_asymmetric=False):
    """
    Calculate and format processing data with proper unit conversions.
    
    Args:
        file_size_kb (float): File size in kilobytes
        raw_rate (float): Raw processing rate (bytes/s for asymmetric, MB/s for symmetric)
        is_asymmetric (bool): Whether the algorithm is asymmetric
    
    Returns:
        dict: Formatted data with proper units and calculations
    """
    file_size_bytes = file_size_kb * 1024
    file_size_mb = file_size_kb / 1024

    # Convert rate to MB/s
    if is_asymmetric:
        rate_mbs = raw_rate / (1024 * 1024)  # Convert bytes/s to MB/s
        estimated_time = file_size_bytes / raw_rate if raw_rate > 0 else 0
    else:
        rate_mbs = raw_rate  # Already in MB/s
        estimated_time = file_size_mb / rate_mbs if rate_mbs > 0 else 0

    return {
        'file_size': {
            'bytes': file_size_bytes,
            'kb': file_size_kb,
            'mb': file_size_mb,
            'display': f"{file_size_bytes:.2f} bytes ({file_size_kb:.2f} KB, {file_size_mb:.6f} MB)"
        },
        'rate': {
            'raw': raw_rate,
            'mb_per_sec': rate_mbs
        },
        'estimated_time': estimated_time
    }
